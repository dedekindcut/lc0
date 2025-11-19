import torch
from torch.utils.data import IterableDataset
import numpy as np
import glob
import os
import chunkparser

class Lc0Dataset(IterableDataset):
    def __init__(self, data_dir, batch_size=256, workers=4, shuffle_size=524288):
        super().__init__()
        self.data_dir = data_dir
        self.batch_size = batch_size
        self.workers = workers
        self.shuffle_size = shuffle_size
        
        # Find all chunk files
        # Lc0 training data is usually in .gz files inside subdirectories
        # e.g. data_dir/game_001.gz or data_dir/subdir/game_001.gz
        # The README says "chunks are packed into a tar file". 
        # Assuming extracted chunks (gz files).
        self.chunks = glob.glob(os.path.join(data_dir, "**", "*.gz"), recursive=True)
        
        if not self.chunks:
            # Try flat directory
            self.chunks = glob.glob(os.path.join(data_dir, "*.gz"))
            
        print(f"Found {len(self.chunks)} chunks.")
        
    def __iter__(self):
        # Create ChunkParser
        # V6 input format is 5 (INPUT_112_WITH_CANONICALIZATION_V2) or similar.
        # We need to know the expected input format.
        # chunkparser constants:
        # V6_STRUCT_STRING
        # But expected_input_format arg is for verification?
        # chunkparser.py: assert input_format == self.expected_input_format
        
        # Let's try format 5 (current default?) or 2?
        # README says "input_format: 2" in some old configs? 
        # Actually, checking recent Lc0 code or configs might help.
        # But let's default to 5 and see if it crashes, or 2.
        # Format 5 is INPUT_112_WITH_CANONICALIZATION_V2.
        
        # We use the internal multiprocessing of ChunkParser.
        # So we shouldn't use PyTorch num_workers > 0 usually.
        
        parser = chunkparser.ChunkParser(
            self.chunks,
            expected_input_format=5, # Try 5 first
            shuffle_size=self.shuffle_size,
            batch_size=self.batch_size,
            workers=self.workers
        )
        
        # Iterating parser.parse() yields batches of BYTES
        for batch_bytes in parser.parse():
            # batch_bytes is tuple: (planes, probs, winner, q, plies_left)
            # unpack
            
            # 1. Planes: float32, shape (B, 112, 8, 8)
            # But they come as flat bytes.
            planes = np.frombuffer(batch_bytes[0], dtype=np.float32)
            planes = planes.reshape(self.batch_size, 112, 8, 8)
            
            # 2. Probs: float32 (probs are stored as float in V6), shape (B, 1858)
            probs = np.frombuffer(batch_bytes[1], dtype=np.float32)
            probs = probs.reshape(self.batch_size, 1858)
            
            # 3. Winner: float32, shape (B, 3) -> (Win, Draw, Loss)?
            # chunkparser: winner = struct.pack('fff', ...)
            winner = np.frombuffer(batch_bytes[2], dtype=np.float32)
            winner = winner.reshape(self.batch_size, 3)
            
            # 4. Q: float32, shape (B, 3) -> (Win_Q, Draw_Q, Loss_Q) or just Q, D, ?
            # chunkparser: best_q = struct.pack('fff', best_q_w, best_d, best_q_l)
            q = np.frombuffer(batch_bytes[3], dtype=np.float32)
            q = q.reshape(self.batch_size, 3)
            
            # 5. Plies left: float32, (B, 1)
            # plies = np.frombuffer(batch_bytes[4], dtype=np.float32)
            # plies = plies.reshape(self.batch_size, 1)
            
            # Convert to Tensor
            yield {
                'input': torch.from_numpy(planes), # (B, 112, 8, 8)
                'policy_target': torch.from_numpy(probs), # (B, 1858)
                'value_target': torch.from_numpy(q), # (B, 3) - usually we train against Q (MCTS result)
                'winner_target': torch.from_numpy(winner) # (B, 3) - Game result
            }
        
        parser.shutdown()
