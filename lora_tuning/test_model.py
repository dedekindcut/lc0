import os
import sys

import torch

import loader
import model


def main():
    if len(sys.argv) < 2:
        print("Usage: python test_model.py <path_to_net.pb.gz>")
        sys.exit(1)

    path = sys.argv[1]
    if not os.path.exists(path):
        print(f"File not found: {path}")
        sys.exit(1)

    print(f"Loading {path}...")
    net_proto = loader.load_proto(path)

    print("Building PyTorch model...")
    lc0_net = model.LC0Net(net_proto)

    print("Model architecture:")
    print(lc0_net)

    # Create dummy input (B, 112, 8, 8)
    x = torch.randn(1, 112, 8, 8)

    print("Running forward pass...")
    p, v = lc0_net(x)

    if p is not None:
        print(f"Policy output shape: {p.shape}")
    else:
        print("Policy output is None (weights not found/implemented)")

    if v is not None:
        print(f"Value output shape: {v.shape}")
        # Only print item if scalar
        if v.numel() == 1:
            print(f"Value output: {v.item()}")
    else:
        print("Value output is None")

    print("Applying LoRA...")
    lc0_net.apply_lora(rank=4, alpha=8)

    print("Running forward pass with LoRA...")
    p_lora, v_lora = lc0_net(x)

    if v_lora is not None and v is not None:
        if v_lora.numel() == 1:
            print(f"Value output (LoRA): {v_lora.item()}")
            print(f"Difference: {v_lora.item() - v.item()}")

    print("Baking LoRA...")
    # save_proto handles baking internally
    output_filename = "badgyal_lora_test.pb.gz"
    print(f"Saving to {output_filename}...")
    lc0_net.save_proto(output_filename)

    print("Loading saved model to verify...")
    net_proto_2 = loader.load_proto(output_filename)
    lc0_net_2 = model.LC0Net(net_proto_2)

    print("Running forward pass on loaded model...")
    p_2, v_2 = lc0_net_2(x)

    if v_2 is not None and v_lora is not None:
        if v_2.numel() == 1:
            print(f"Value output (Reloaded): {v_2.item()}")
            print(f"Difference (LoRA - Reloaded): {v_lora.item() - v_2.item()}")

    # Cleanup
    if os.path.exists(output_filename):
        os.remove(output_filename)


if __name__ == "__main__":
    main()
