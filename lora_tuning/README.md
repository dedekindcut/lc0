# Lc0 LoRA Tuning

This directory contains tools to fine-tune Leela Chess Zero (Lc0) networks using Low-Rank Adaptation (LoRA).

## Features
- **Dynamic Model Loading**: Loads `lc0` protobuf network files (`.pb.gz`) directly into PyTorch.
- **ResNet & Transformer Support**: Supports standard Lc0 ResNets (like `badgyal`) and newer Transformers (like `BT4`).
- **LoRA Implementation**: Adds LoRA adapters to Conv2d and Linear layers.
- **Baking**: Merges LoRA weights back into the base network and saves valid `.pb.gz` files that can be run by the standard `lc0` binary.

## Usage

### Prerequisites
```bash
uv add torch numpy protobuf grpcio-tools
```

### 1. Compile Protobuf
Before running, ensure `net_pb2.py` is generated:
```bash
uv run python -m grpc_tools.protoc -I../proto --python_out=. ../proto/net.proto
```

### 2. Load and Inspect a Network
```bash
uv run loader.py path/to/network.pb.gz
```

### 3. Run LoRA Test (Load -> Apply LoRA -> Bake -> Save)
```bash
uv run test_model.py path/to/network.pb.gz
```

### 4. Prepare Data
The C++ dataloader requires data to be split into manageable chunks (to avoid OOM on large files).
If you have a single large `train_data.gz`, run:
```bash
uv run split_data.py
```
This will create `data/chunks/`.

### 5. Train
```bash
uv run train.py --network tuned_badgyal.pb.gz --data data --output tuned.pb.gz --batch_size 256 --steps 1000
```

## Files
- `loader.py`: Handles reading/writing Lc0 protobuf weights and quantizing/dequantizing.
- `model.py`: PyTorch model definition (Lc0Net, LoRALayer, MHA, etc.) that mirrors the Lc0 C++ inference code.
- `test_model.py`: Verification script.
- `train.py`: Training loop using LoRA.
- `dataset.py`: PyTorch IterableDataset wrapping the high-performance C++ dataloader.
- `lczero_training/`: Compiled C++ dataloader extension (from `lc0-training`).
- `split_data.py`: Helper to split large training files.
