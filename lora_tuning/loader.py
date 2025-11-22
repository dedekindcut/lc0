import gzip
import os
import sys

import numpy as np

# Ensure we can import the generated protobuf file
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
try:
    import net_pb2
except ImportError:
    print("Error: net_pb2.py not found. Did you compile the protobufs?")
    sys.exit(1)


def load_proto(filename):
    """Reads a compressed or uncompressed protobuf file."""
    try:
        with gzip.open(filename, "rb") as f:
            data = f.read()
    except gzip.BadGzipFile:
        with open(filename, "rb") as f:
            data = f.read()

    net = net_pb2.Net()
    net.ParseFromString(data)
    return net


def decode_layer(layer):
    """Decodes a Weight layer proto into a numpy float array."""
    if not layer.HasField("params"):
        return None

    # Get raw bytes
    raw_data = layer.params

    # Determine encoding
    encoding = (
        layer.encoding if layer.HasField("encoding") else net_pb2.Weights.Layer.LINEAR16
    )

    if encoding == net_pb2.Weights.Layer.LINEAR16:
        # Read as uint16
        uint16_data = np.frombuffer(raw_data, dtype=np.uint16)

        # Dequantize: val = min + (max - min) * (int_val / 65535)
        min_val = layer.min_val
        max_val = layer.max_val

        # Convert to float
        float_data = uint16_data.astype(np.float32) / 65535.0
        return min_val + (max_val - min_val) * float_data

    elif encoding == net_pb2.Weights.Layer.FLOAT16:
        return np.frombuffer(raw_data, dtype=np.float16).astype(np.float32)

    else:
        raise ValueError(f"Unsupported encoding: {encoding}")


def encode_layer(data, encoding=net_pb2.Weights.Layer.LINEAR16):
    """Encodes a numpy float array into a Weights.Layer proto."""
    layer = net_pb2.Weights.Layer()

    # Flatten
    flat_data = data.flatten().astype(np.float32)

    if encoding == net_pb2.Weights.Layer.LINEAR16:
        min_val = float(flat_data.min())
        max_val = float(flat_data.max())

        layer.min_val = min_val
        layer.max_val = max_val
        layer.encoding = net_pb2.Weights.Layer.LINEAR16

        # Quantize
        if max_val == min_val:
            # All same, avoid div by zero
            quantized = np.zeros_like(flat_data, dtype=np.uint16)
        else:
            scale = 65535.0 / (max_val - min_val)
            quantized = ((flat_data - min_val) * scale).astype(np.uint16)

        layer.params = quantized.tobytes()

    elif encoding == net_pb2.Weights.Layer.FLOAT16:
        layer.encoding = net_pb2.Weights.Layer.FLOAT16
        layer.params = flat_data.astype(np.float16).tobytes()

    else:
        raise ValueError(f"Unsupported encoding: {encoding}")

    return layer


def describe_net(net):
    """Prints the structure of the network."""
    if not net.HasField("weights"):
        print("No weights in this file (maybe ONNX model?)")
        return

    w = net.weights

    print("Network Structure:")

    # Input
    if w.HasField("input"):
        l = w.input
        # Check conv block
        if l.HasField("weights"):
            d = decode_layer(l.weights)
            print(f"  Input Conv: {d.shape} (params={d.size})")

    # Residual Tower
    if len(w.residual) > 0:
        print(f"  Residual Blocks: {len(w.residual)}")
        for i, res in enumerate(w.residual):
            # Just check the first one to keep output short
            if i == 0:
                if res.HasField("conv1"):
                    c1 = decode_layer(res.conv1.weights)
                    if c1 is not None:
                        print(f"    Block 0 Conv1: {c1.shape}")
                        if res.conv1.HasField("biases"):
                            print(
                                f"      Has biases: {decode_layer(res.conv1.biases).shape}"
                            )
                        if res.conv1.HasField("bn_means"):
                            print("      Has BN means")
                if res.HasField("conv2"):
                    c2 = decode_layer(res.conv2.weights)
                    if c2 is not None:
                        print(f"    Block 0 Conv2: {c2.shape}")
                if res.HasField("se"):
                    print("    Block 0 has SE unit")

    # Encoder Stack (Transformers/AttentionBody)
    if len(w.encoder) > 0:
        print(f"  Encoder Blocks: {len(w.encoder)}")
        # Check input embedding
        if w.HasField("ip_emb_w"):
            emb = decode_layer(w.ip_emb_w)
            print(f"  Input Embedding: {emb.shape}")
        if w.HasField("ip_emb_preproc_w"):
            print("  Has Input Preproc (LayerNorm?)")

        # Check first block
        e = w.encoder[0]
        if e.HasField("mha"):
            print("    Block 0 has MHA")
            if e.mha.HasField("q_w"):
                print(f"      Q Weights: {decode_layer(e.mha.q_w).shape}")
            if e.mha.HasField("rpe_q"):
                print(f"      Has RPE_Q: {decode_layer(e.mha.rpe_q).shape}")
            if e.mha.HasField("rpe_k"):
                print(f"      Has RPE_K: {decode_layer(e.mha.rpe_k).shape}")
        if e.HasField("ffn"):
            print("    Block 0 has FFN")

    # Policy Head
    if w.HasField("policy"):
        p = decode_layer(w.policy.weights)
        if p is not None:
            print(f"  Policy Head Conv: {p.shape}")
        else:
            print("  Policy Head Conv: (weights missing in proto?)")
        # Check params
        if w.policy.HasField("bn_means"):
            print("    Has BN")

    # Policy Format
    if net.HasField("format") and net.format.HasField("network_format"):
        print(f"  Policy Format: {net.format.network_format.policy}")

    # Policy Head FC
    if w.HasField("ip_pol_w"):
        pw = decode_layer(w.ip_pol_w)
        print(f"  Policy FC Weight: {pw.shape}")

    if w.HasField("policy_heads"):
        print("  Has PolicyHeads message")
        ph = w.policy_heads
        if ph.HasField("vanilla"):
            print("    Has vanilla policy head")

    if w.HasField("ip2_pol_w"):
        pw2 = decode_layer(w.ip2_pol_w)
        print(f"  Policy FC2 Weight: {pw2.shape}")

    # Value Head
    if w.HasField("value"):
        v = decode_layer(w.value.weights)
        print(f"  Value Head Conv: {v.shape}")

    # Value Head FC
    if w.HasField("ip1_val_w"):
        vw = decode_layer(w.ip1_val_w)
        print(f"  Value FC1 Weight: {vw.shape}")
    if w.HasField("ip2_val_w"):
        vw2 = decode_layer(w.ip2_val_w)
        print(f"  Value FC2 Weight: {vw2.shape}")
    if w.HasField("ip_val_w"):
        vw3 = decode_layer(w.ip_val_w)
        print(f"  Value FC (ip_val) Weight: {vw3.shape}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python loader.py <path_to_net.pb.gz>")
        sys.exit(1)

    path = sys.argv[1]
    if not os.path.exists(path):
        print(f"File not found: {path}")
        sys.exit(1)

    print(f"Loading {path}...")
    net = load_proto(path)
    describe_net(net)
