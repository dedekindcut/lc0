import argparse
import os

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.utils.data import DataLoader

import dataset
import loader
import model


def train(args):
    # 1. Load Base Network
    print(f"Loading network from {args.network}...")
    net_proto = loader.load_proto(args.network)
    lc0_net = model.LC0Net(net_proto)

    # Move to GPU if available
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    if torch.backends.mps.is_available():
        device = torch.device("mps")
    print(f"Using device: {device}")

    lc0_net.to(device)

    # 2. Apply LoRA
    print(f"Applying LoRA (rank={args.rank}, alpha={args.alpha})...")
    lc0_net.apply_lora(rank=args.rank, alpha=args.alpha)
    lc0_net.to(device)  # Ensure new params are on device

    # Verify only LoRA params are trainable
    trainable_params = 0
    all_params = 0
    for p in lc0_net.parameters():
        all_params += p.numel()
        if p.requires_grad:
            trainable_params += p.numel()
    print(
        f"Trainable params: {trainable_params} / {all_params} ({trainable_params / all_params:.2%})"
    )

    # 3. Setup Data
    input_format = 5  # Default if not found
    if net_proto.HasField("format") and net_proto.format.HasField("network_format"):
        input_format = net_proto.format.network_format.input

    print(f"Initializing dataset from {args.data}...")
    ds = dataset.Lc0Dataset(
        args.data,
        batch_size=args.batch_size,
        workers=args.workers,
        input_format=input_format,
    )
    # Using num_workers=0 because C++ Loader manages its own processes
    train_loader = DataLoader(ds, batch_size=None, num_workers=0)

    # 4. Optimizer
    optimizer = optim.AdamW(lc0_net.parameters(), lr=args.lr, weight_decay=1e-4)

    # 5. Training Loop
    step = 0
    for batch in train_loader:
        step += 1

        # Move data to device
        x = batch["input"].to(device)
        policy_target = batch["policy_target"].to(device)
        value_target = batch["value_target"].to(device)  # (B, 3)

        # Forward pass
        p_pred, v_pred = lc0_net(x)

        loss = 0
        logs = {}

        # Policy Loss
        # p_pred: (B, 1858) logits
        # policy_target: (B, 1858) probabilities
        if p_pred is not None:
            # Flatten if needed (B, C, H, W) -> (B, 1858)
            if len(p_pred.shape) == 4:
                p_pred = p_pred.flatten(1)

            if p_pred.shape == policy_target.shape:
                # Target is probabilities, prediction is logits
                log_probs = torch.log_softmax(p_pred, dim=1)
                pol_loss = -(policy_target * log_probs).sum(dim=1).mean()
                loss += args.policy_weight * pol_loss
                logs["pol_loss"] = pol_loss.item()

        # Value Loss
        if v_pred is not None:
            # v_pred: (B, 1) scalar or (B, 3) WDL logits
            if v_pred.shape[1] == 1:
                # Scalar tanh output
                # Target: Q value from (W, D, L) -> Q = W - L
                target_q = value_target[:, 0] - value_target[:, 2]
                target_q = target_q.view(-1, 1)

                val_loss = F.mse_loss(v_pred, target_q)
                loss += args.value_weight * val_loss
                logs["val_loss"] = val_loss.item()
            elif v_pred.shape[1] == 3:
                # WDL logits
                # Target: (W, D, L) probabilities
                log_probs = torch.log_softmax(v_pred, dim=1)
                val_loss = -(value_target * log_probs).sum(dim=1).mean()
                loss += args.value_weight * val_loss
                logs["val_loss"] = val_loss.item()

        # Backward pass
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        if step % 10 == 0:
            log_str = f"Step {step}: Loss {loss.item():.4f}"
            for k, v in logs.items():
                log_str += f" | {k}: {v:.4f}"
            print(log_str)

        if step >= args.steps:
            break

    # 6. Save
    print(f"Saving fine-tuned model to {args.output}...")
    lc0_net.save_proto(args.output)
    print("Done.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--network", required=True, help="Path to base .pb.gz network")
    parser.add_argument(
        "--data", required=True, help="Path to training data chunks dir"
    )
    parser.add_argument("--output", required=True, help="Path to save output .pb.gz")
    parser.add_argument("--rank", type=int, default=4, help="LoRA rank")
    parser.add_argument("--alpha", type=float, default=8, help="LoRA alpha")
    parser.add_argument("--lr", type=float, default=1e-4, help="Learning rate")
    parser.add_argument("--steps", type=int, default=1000, help="Training steps")
    parser.add_argument("--batch_size", type=int, default=256, help="Batch size")
    parser.add_argument(
        "--workers", type=int, default=4, help="Number of worker processes"
    )
    parser.add_argument(
        "--policy_weight", type=float, default=1.0, help="Policy loss weight"
    )
    parser.add_argument(
        "--value_weight", type=float, default=1.0, help="Value loss weight"
    )

    args = parser.parse_args()
    train(args)
