# Lc0 LoRA Tuning

This repository provides a **self-contained** pipeline for fine-tuning Leela Chess Zero (Lc0) networks using Low-Rank Adaptation (LoRA). It includes a high-performance C++ dataloader, supports standard ResNets and newer Transformers (BT4/BT5), and can handle Relative Positional Encodings (RPE).

## Features
- **Self-Contained**: No need to clone external Lc0 training repos. All C++ sources and build configs are included.
- **High-Performance Dataloader**: Multithreaded C++ dataloader (via `lczero_training` extension) reads Lc0 binary data (V6/V7) efficiently.
- **LoRA Support**: Freezes the backbone and trains lightweight adapters for Attention/Conv layers.
- **Architecture Support**:
    - **ResNet** (e.g., `badgyal`)
    - **Transformer** (e.g., `BT4`, `BT5`) with RPE support.
- **Baking**: Merges LoRA weights back into `.pb.gz` format compatible with standard `lc0` binaries.

## Quick Start

### 1. Install Dependencies
**Linux (Ubuntu/Debian)**:
```bash
sudo apt update
sudo apt install -y pkg-config python3-pybind11 pybind11-dev libz-dev libgtest-dev protobuf-compiler
```

**macOS**:
```bash
brew install pkg-config protobuf meson ninja
```

**Python Dependencies**:
```bash
# Install uv if you haven't: curl -LsSf https://astral.sh/uv/install.sh | sh
uv sync
```

### 2. Build C++ Extension
This compiles the dataloader and protobuf definitions. Run these commands from the `lora_tuning` directory:

```bash
# 1. Setup Build
uv run meson setup build/release/ --buildtype=release

# 2. Compile
uv run meson compile -C build/release/

# 3. Generate Protobufs
mkdir -p src/proto
touch src/proto/__init__.py
uv run python -m grpc_tools.protoc --proto_path=. --proto_path=libs/lc0 --python_out=src/ --pyi_out=src/ proto/*.proto
uv run python -m grpc_tools.protoc --proto_path=. --proto_path=libs/lc0 --python_out=src/ --pyi_out=src/ proto/net.proto proto/onnx.proto proto/hlo.proto

# 4. Link Extension
mkdir -p lczero_training
# Copy the compiled .so file (name varies by OS)
cp build/release/_lczero_training.*.so lczero_training/_lczero_training.so
```

### 3. Prepare Data
Your training data should be in Lc0 binary format (`.gz` files).
*   If you have a single massive file (e.g., `train_data.gz` > 1GB), split it:
    ```bash
    uv run scripts/split_data.py
    ```
*   If you have many small `.gz` files (e.g. from `QueenOddsV2`), just point the trainer to the directory containing them.

### 4. Train
```bash
uv run train.py \
    --network nets/BT5-1024x15x32h-rpe-swa-3700000.pb.gz \
    --data data/chunks \
    --output tuned_bt5.pb.gz \
    --batch_size 256 \
    --steps 10000 \
    --lr 1e-4 \
    --alpha 0.5
```

### 5. Test / Verify
To verify the trained model architecture or run a dummy forward pass:
```bash
uv run test_model.py tuned_bt5.pb.gz
```

## File Structure
*   `csrc/`, `libs/`, `subprojects/`: C++ source code for the dataloader.
*   `train.py`: Main training loop.
*   `model.py`: PyTorch implementation of Lc0 architectures (ResNet/Transformer/LoRA/RPE).
*   `dataset.py`: Wrapper for the C++ dataloader.
*   `loader.py`: Utilities for reading/writing Lc0 `.pb.gz` files.
*   `scripts/`: Helper scripts (splitting data, testing imports).

## Troubleshooting
*   **`invalid ELF header`**: You are trying to run a `.so` compiled on macOS on Linux (or vice versa). Re-run the "Build C++ Extension" steps on the target machine.
*   **`Dependency lookup for pybind11 failed`**: Ensure you installed `python3-pybind11` and `pkg-config`.
*   **`meson build directory` error**: If you moved the folder or changed envs, delete `build/` and run `meson setup` again.
