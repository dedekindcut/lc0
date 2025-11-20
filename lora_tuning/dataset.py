import torch
from torch.utils.data import IterableDataset
import numpy as np
import os
import sys

# Ensure we can import the C++ extension and protobufs
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from lczero_training import _lczero_training
    from proto import data_loader_config_pb2
except ImportError as e:
    print(f"Error importing lczero_training or proto: {e}")
    print("Make sure _lczero_training.so and proto/ are in the python path.")
    raise

class Lc0Dataset(IterableDataset):
    def __init__(self, data_dir, batch_size=256, workers=4, shuffle_size=524288, input_format=5):
        super().__init__()
        self.data_dir = data_dir
        self.batch_size = batch_size
        self.workers = workers
        self.shuffle_size = shuffle_size
        self.input_format = input_format
        self.loader = None

    def _init_loader(self):
        config = data_loader_config_pb2.DataLoaderConfig()
        
        # Stage 1: File Path Provider
        stage_fpp = config.stage.add()
        stage_fpp.name = "file_path_provider"
        stage_fpp.file_path_provider.directory = self.data_dir
        stage_fpp.file_path_provider.output.queue_capacity = 16

        # Stage 2: Chunk Source Loader
        stage_csl = config.stage.add()
        stage_csl.name = "chunk_source_loader"
        stage_csl.input.append("file_path_provider")
        stage_csl.chunk_source_loader.threads = max(1, self.workers // 2)
        stage_csl.chunk_source_loader.output.queue_capacity = 16

        # Stage 3: Shuffling Chunk Pool
        stage_scp = config.stage.add()
        stage_scp.name = "shuffling_chunk_pool"
        stage_scp.input.append("chunk_source_loader")
        # Use a reasonable pool size based on shuffle_size
        # Assuming 1 chunk is roughly 1000 positions (standard V6/V7 chunk size varies)
        # shuffle_size is in positions.
        stage_scp.shuffling_chunk_pool.chunk_pool_size = min(500, self.shuffle_size // 1000 + 1) 
        stage_scp.shuffling_chunk_pool.source_ingestion_threads = 1
        stage_scp.shuffling_chunk_pool.chunk_loading_threads = max(1, self.workers)
        stage_scp.shuffling_chunk_pool.output.queue_capacity = 16
        
        # Stage 4: Chunk Unpacker
        stage_cu = config.stage.add()
        stage_cu.name = "chunk_unpacker"
        stage_cu.input.append("shuffling_chunk_pool")
        stage_cu.chunk_unpacker.threads = max(1, self.workers)
        stage_cu.chunk_unpacker.position_sampling_rate = 1.0 # Use all positions
        stage_cu.chunk_unpacker.output.queue_capacity = 16

        # Stage 5: Shuffling Frame Sampler
        stage_sfs = config.stage.add()
        stage_sfs.name = "shuffling_frame_sampler"
        stage_sfs.input.append("chunk_unpacker")
        stage_sfs.shuffling_frame_sampler.threads = max(1, self.workers)
        # Reservoir size per thread
        stage_sfs.shuffling_frame_sampler.reservoir_size_per_thread = 1000
        stage_sfs.shuffling_frame_sampler.output.queue_capacity = 16

        # Stage 6: Tensor Generator
        stage_tg = config.stage.add()
        stage_tg.name = "tensor_generator"
        stage_tg.input.append("shuffling_frame_sampler")
        stage_tg.tensor_generator.threads = max(1, self.workers)
        stage_tg.tensor_generator.batch_size = self.batch_size
        stage_tg.tensor_generator.output.queue_capacity = 16

        config.output.append("tensor_generator")

        print("Initializing C++ DataLoader...")
        self.loader = _lczero_training.DataLoader(config)
        self.loader.start()

    def __iter__(self):
        if self.loader is None:
            self._init_loader()
            
        while True:
            # Returns tuple of numpy arrays
            try:
                batch = self.loader.get_next()
            except Exception as e:
                print(f"DataLoader finished or error: {e}")
                break
                
            if batch is None:
                break

            # Map to expected keys
            # batch[0]: Input planes (B, 112, 8, 8) or flat
            # batch[1]: Policy (B, 1858)
            # batch[2]: Value/WDL (B, 3)
            
            planes = batch[0]
            probs = batch[1]
            wdl = batch[2]
            
            # Planes
            if planes.ndim == 2:
                # (B, 112*64) -> (B, 112, 8, 8)
                planes = planes.reshape(-1, 112, 8, 8)
            
            result = {
                'input': torch.from_numpy(planes),
                'policy_target': torch.from_numpy(probs),
                'value_target': torch.from_numpy(wdl),
                'winner_target': torch.from_numpy(wdl)
            }
            
            yield result

