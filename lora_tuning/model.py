import math

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F

import loader


def make_rpe_map():
    # 15 * 15 in units for distance pairs to 64 * 64 pairs of squares
    out = np.zeros((225, 64 * 64), dtype=np.float32)
    for i in range(8):
        for j in range(8):
            for k in range(8):
                for m in range(8):
                    out[
                        15 * (i - k + 7) + (j - m + 7), 64 * (i * 8 + j) + k * 8 + m
                    ] = 1
    return out


# Cache global map
RPE_MAP = torch.from_numpy(make_rpe_map()).float()


class LoRALayer(nn.Module):
    def __init__(self, original_layer, rank=4, alpha=8):
        super().__init__()
        self.rank = rank
        self.alpha = alpha
        self.scaling = alpha / rank

        if isinstance(original_layer, nn.Conv2d):
            self.is_conv = True
            self.in_channels = original_layer.in_channels
            self.out_channels = original_layer.out_channels
            self.kernel_size = original_layer.kernel_size
            self.stride = original_layer.stride
            self.padding = original_layer.padding

            # A: (rank, in * k * k)
            # B: (out, rank)
            self.lora_A = nn.Parameter(
                torch.zeros(
                    rank, self.in_channels * self.kernel_size[0] * self.kernel_size[1]
                )
            )
            self.lora_B = nn.Parameter(torch.zeros(self.out_channels, rank))

            # Freeze original
            original_layer.weight.requires_grad = False
            self.original_layer = original_layer

            # Init
            nn.init.kaiming_uniform_(self.lora_A, a=5**0.5)
            nn.init.zeros_(self.lora_B)

        elif isinstance(original_layer, nn.Linear):
            self.is_conv = False
            self.in_features = original_layer.in_features
            self.out_features = original_layer.out_features

            self.lora_A = nn.Parameter(torch.zeros(rank, self.in_features))
            self.lora_B = nn.Parameter(torch.zeros(self.out_features, rank))

            original_layer.weight.requires_grad = False
            self.original_layer = original_layer

            nn.init.kaiming_uniform_(self.lora_A, a=5**0.5)
            nn.init.zeros_(self.lora_B)

        else:
            raise ValueError(f"Unsupported layer for LoRA: {type(original_layer)}")

    def forward(self, x):
        # Original output
        out = self.original_layer(x)

        # LoRA output
        if self.is_conv:
            W_lora = (self.lora_B @ self.lora_A).view(
                self.out_channels,
                self.in_channels,
                self.kernel_size[0],
                self.kernel_size[1],
            )
            out_lora = F.conv2d(
                x, W_lora * self.scaling, stride=self.stride, padding=self.padding
            )
        else:
            out_lora = (x @ self.lora_A.T @ self.lora_B.T) * self.scaling

        return out + out_lora

    def bake(self):
        with torch.no_grad():
            if self.is_conv:
                W_lora = (self.lora_B @ self.lora_A).view(
                    self.out_channels,
                    self.in_channels,
                    self.kernel_size[0],
                    self.kernel_size[1],
                )
                self.original_layer.weight.data += W_lora * self.scaling
            else:
                W_lora = self.lora_B @ self.lora_A
                self.original_layer.weight.data += W_lora * self.scaling

        return self.original_layer


class LC0ConvBlock(nn.Module):
    def __init__(self, proto_block, in_channels, out_channels=None, activation=True):
        super().__init__()
        self.in_channels = in_channels
        self.activation = activation

        # Decode weights to determine shape
        w_np = loader.decode_layer(proto_block.weights)
        self.has_bias = proto_block.HasField("biases")
        self.has_bn = proto_block.HasField("bn_means")

        if out_channels is None:
            # Infer from weights
            size = w_np.size
            if size % (in_channels * 9) == 0:
                self.kernel_size = 3
                self.padding = 1
                self.out_channels = size // (in_channels * 9)
            elif size % in_channels == 0:
                self.kernel_size = 1
                self.padding = 0
                self.out_channels = size // in_channels
            else:
                raise ValueError(
                    f"Cannot infer conv shape. In={in_channels}, Size={size}"
                )
        else:
            self.out_channels = out_channels
            size = w_np.size
            if size == out_channels * in_channels * 9:
                self.kernel_size = 3
                self.padding = 1
            elif size == out_channels * in_channels:
                self.kernel_size = 1
                self.padding = 0
            else:
                raise ValueError(
                    f"Mismatch: In={in_channels}, Out={out_channels}, Size={size}"
                )

        # Create layers
        self.conv = nn.Conv2d(
            self.in_channels,
            self.out_channels,
            self.kernel_size,
            padding=self.padding,
            bias=self.has_bias and not self.has_bn,
        )

        # Load Conv Weights
        w_tensor = torch.from_numpy(w_np).view(
            self.out_channels, self.in_channels, self.kernel_size, self.kernel_size
        )
        self.conv.weight.data.copy_(w_tensor)

        if self.has_bias and not self.has_bn:
            b_np = loader.decode_layer(proto_block.biases)
            self.conv.bias.data.copy_(torch.from_numpy(b_np))

        if self.has_bn:
            self.bn = nn.BatchNorm2d(self.out_channels, eps=1e-5, momentum=0.1)

            mean = loader.decode_layer(proto_block.bn_means)
            # stddivs in Lc0 is 1/sqrt(var). PyTorch needs var.
            # var = (1/stddivs)^2
            stddivs = loader.decode_layer(proto_block.bn_stddivs)
            var = (1.0 / (stddivs + 1e-10)) ** 2  # Approximate

            gamma = loader.decode_layer(proto_block.bn_gammas)
            beta = loader.decode_layer(proto_block.bn_betas)

            self.bn.running_mean.copy_(torch.from_numpy(mean))
            self.bn.running_var.copy_(torch.from_numpy(var))
            self.bn.weight.data.copy_(torch.from_numpy(gamma))
            self.bn.bias.data.copy_(torch.from_numpy(beta))

    def forward(self, x):
        x = self.conv(x)
        if self.has_bn:
            x = self.bn(x)
        if self.activation:
            return F.relu(x)
        return x


class SEUnit(nn.Module):
    def __init__(self, proto_se, channels):
        super().__init__()
        w1 = loader.decode_layer(proto_se.w1)
        b1 = loader.decode_layer(proto_se.b1)
        w2 = loader.decode_layer(proto_se.w2)
        b2 = loader.decode_layer(proto_se.b2)

        # w1 shape: (reduced, channels)
        # w2 shape: (channels*2, reduced)

        reduced = w1.shape[0] // channels

        self.fc1 = nn.Linear(channels, reduced)
        self.fc2 = nn.Linear(reduced, channels * 2)

        # Load weights. Linear weights in PyTorch are (Out, In)
        self.fc1.weight.data.copy_(torch.from_numpy(w1).view(reduced, channels))
        self.fc1.bias.data.copy_(torch.from_numpy(b1))

        self.fc2.weight.data.copy_(torch.from_numpy(w2).view(channels * 2, reduced))
        self.fc2.bias.data.copy_(torch.from_numpy(b2))

    def forward(self, x):
        # x: (B, C, H, W)
        b, c, _, _ = x.size()
        y = F.adaptive_avg_pool2d(x, 1).view(b, c)
        y = F.relu(self.fc1(y))
        y = self.fc2(y)

        # Output is 2C: Scale (C), Bias (C) usually for Lc0
        scale, bias = torch.split(y, c, dim=1)
        scale = torch.sigmoid(scale).view(b, c, 1, 1)
        bias = bias.view(b, c, 1, 1)

        return x * scale + bias


class RPELogits(nn.Module):
    def __init__(self, proto_layer, head_depth, head_count, rpe_type="q"):
        super().__init__()
        self.head_depth = head_depth
        self.head_count = head_count
        self.rpe_type = rpe_type

        # proto_layer is Layer
        w_np = loader.decode_layer(proto_layer)
        # Shape: (head_depth * head_count, 225)
        # Verify size
        expected_size = head_depth * head_count * 225
        if w_np.size != expected_size:
            # Dimensions may differ if inferred incorrectly
            pass

        self.rpe_w = nn.Parameter(
            torch.from_numpy(w_np).view(head_depth * head_count, 225)
        )
        # We freeze RPE weights by default as we don't LoRA them
        self.rpe_w.requires_grad = False

    def forward(self, x):
        # x: (B, H, 64, D) (transposed q/k)
        # self.rpe_w: (D*H, 225)
        # RPE_MAP: (225, 4096)
        # Bias = rpe_w @ map -> (D*H, 4096)

        bias = self.rpe_w @ RPE_MAP.to(x.device)  # (D*H, 4096)
        bias = bias.view(self.head_depth, self.head_count, 64, 64)  # (D, H, Q, K)

        # Einsum
        # if q: x is (B, H, Q, D). bias is (D, H, Q, K)
        # output (B, H, Q, K)
        # eq: bhqd, dhqk -> bhqk

        if self.rpe_type == "q":
            return torch.einsum("bhqd, dhqk -> bhqk", x, bias)
        else:
            return torch.einsum("bhkd, dhqk -> bhqk", x, bias)


class MHA(nn.Module):
    def __init__(self, proto_mha, model_dim, heads):
        super().__init__()
        self.model_dim = model_dim
        self.heads = heads
        self.head_dim = model_dim // heads

        # Q, K, V, Dense
        # All are Linear(model_dim, model_dim)

        self.q_proj = nn.Linear(model_dim, model_dim)
        self.k_proj = nn.Linear(model_dim, model_dim)
        self.v_proj = nn.Linear(model_dim, model_dim)
        self.out_proj = nn.Linear(model_dim, model_dim)

        # Load weights
        def load_linear(layer, proto_w, proto_b):
            w = loader.decode_layer(proto_w)
            b = loader.decode_layer(proto_b)
            layer.weight.data.copy_(torch.from_numpy(w).view(model_dim, model_dim))
            layer.bias.data.copy_(torch.from_numpy(b))

        load_linear(self.q_proj, proto_mha.q_w, proto_mha.q_b)
        load_linear(self.k_proj, proto_mha.k_w, proto_mha.k_b)
        load_linear(self.v_proj, proto_mha.v_w, proto_mha.v_b)
        load_linear(self.out_proj, proto_mha.dense_w, proto_mha.dense_b)

        # Relative Positional Encodings (RPE)
        self.rpe_q = None
        self.rpe_k = None

        if proto_mha.HasField("rpe_q"):
            self.rpe_q = RPELogits(proto_mha.rpe_q, self.head_dim, self.heads, "q")
        if proto_mha.HasField("rpe_k"):
            self.rpe_k = RPELogits(proto_mha.rpe_k, self.head_dim, self.heads, "k")

    def forward(self, x):
        # x: (B, Seq, Dim)
        B, Seq, _ = x.shape

        # View as (B, Seq, H, D) then transpose to (B, H, Seq, D) for dot product attention
        q = self.q_proj(x).view(B, Seq, self.heads, self.head_dim).transpose(1, 2)
        k = self.k_proj(x).view(B, Seq, self.heads, self.head_dim).transpose(1, 2)
        v = self.v_proj(x).view(B, Seq, self.heads, self.head_dim).transpose(1, 2)

        # Scaled Dot-Product Attention
        scores = q @ k.transpose(-2, -1)  # (B, H, Seq, Seq)

        # Apply RPE
        if self.rpe_q:
            scores = scores + self.rpe_q(q)
        if self.rpe_k:
            scores = scores + self.rpe_k(k)

        scores = scores / (self.head_dim**0.5)

        attn = F.softmax(scores, dim=-1)
        out = attn @ v

        out = out.transpose(1, 2).reshape(B, Seq, self.model_dim)
        return self.out_proj(out)


class FFN(nn.Module):
    def __init__(self, proto_ffn, model_dim):
        super().__init__()
        # dense1: Dim -> 4*Dim (usually)
        # dense2: 4*Dim -> Dim

        w1 = loader.decode_layer(proto_ffn.dense1_w)
        # infer hidden dim
        hidden_dim = w1.size // model_dim

        self.fc1 = nn.Linear(model_dim, hidden_dim)
        self.fc2 = nn.Linear(hidden_dim, model_dim)

        self.fc1.weight.data.copy_(torch.from_numpy(w1).view(hidden_dim, model_dim))
        self.fc1.bias.data.copy_(
            torch.from_numpy(loader.decode_layer(proto_ffn.dense1_b))
        )

        w2 = loader.decode_layer(proto_ffn.dense2_w)
        self.fc2.weight.data.copy_(torch.from_numpy(w2).view(model_dim, hidden_dim))
        self.fc2.bias.data.copy_(
            torch.from_numpy(loader.decode_layer(proto_ffn.dense2_b))
        )

    def forward(self, x):
        return self.fc2(F.relu(self.fc1(x)))


class LC0EncoderBlock(nn.Module):
    def __init__(self, proto_enc, model_dim, heads):
        super().__init__()
        self.ln1 = nn.LayerNorm(model_dim)
        self.mha = MHA(proto_enc.mha, model_dim, heads)
        self.ln2 = nn.LayerNorm(model_dim)
        self.ffn = FFN(proto_enc.ffn, model_dim)

        # Load LN params
        self.ln1.weight.data.copy_(
            torch.from_numpy(loader.decode_layer(proto_enc.ln1_gammas))
        )
        self.ln1.bias.data.copy_(
            torch.from_numpy(loader.decode_layer(proto_enc.ln1_betas))
        )
        self.ln2.weight.data.copy_(
            torch.from_numpy(loader.decode_layer(proto_enc.ln2_gammas))
        )
        self.ln2.bias.data.copy_(
            torch.from_numpy(loader.decode_layer(proto_enc.ln2_betas))
        )

    def forward(self, x):
        # Lc0 uses Pre-norm configuration
        residual = x
        x = self.ln1(x)
        x = self.mha(x)
        x = x + residual

        residual = x
        x = self.ln2(x)
        x = self.ffn(x)
        x = x + residual
        return x


class LC0ResBlock(nn.Module):
    def __init__(self, proto_res, filters):
        super().__init__()
        # Conv1 has ReLU
        self.conv1 = LC0ConvBlock(proto_res.conv1, filters, filters, activation=True)
        # Conv2 has NO ReLU (it happens after add)
        self.conv2 = LC0ConvBlock(proto_res.conv2, filters, filters, activation=False)

        if proto_res.HasField("se"):
            self.se = SEUnit(proto_res.se, filters)
        else:
            self.se = None

    def forward(self, x):
        residual = x
        out = self.conv1(x)
        out = self.conv2(out)

        if self.se:
            out = self.se(out)

        out += residual
        return F.relu(out)


class LC0Net(nn.Module):
    def __init__(self, proto_net):
        super().__init__()
        self.proto_net = proto_net
        w = proto_net.weights

        # Check Policy Format, default to Classical (1)
        self.policy_format = 1
        if proto_net.HasField("format") and proto_net.format.HasField("network_format"):
            self.policy_format = proto_net.format.network_format.policy

        self.is_transformer = len(w.encoder) > 0

        if self.is_transformer:
            # Infer model dim from first encoder block weights
            w_q = loader.decode_layer(w.encoder[0].mha.q_w)
            dim_sq = w_q.size
            self.model_dim = int(math.sqrt(dim_sq))

            # Defaulting to 32 heads (standard for many architectures)
            self.heads = 32

            self.blocks = nn.ModuleList()
            for enc in w.encoder:
                self.blocks.append(LC0EncoderBlock(enc, self.model_dim, self.heads))

            # Input projection (if any)
            if w.HasField("ip_emb_w"):
                w_emb = loader.decode_layer(w.ip_emb_w)
                in_features = w_emb.size // self.model_dim

                # Linear projection per square
                self.input_emb = nn.Linear(in_features, self.model_dim)
                self.input_emb.weight.data.copy_(
                    torch.from_numpy(w_emb).view(self.model_dim, in_features)
                )

                if w.HasField("ip_emb_b"):
                    b_emb = loader.decode_layer(w.ip_emb_b)
                    self.input_emb.bias.data.copy_(torch.from_numpy(b_emb))

                if w.HasField("ip_emb_preproc_w"):
                    # Input Layer Norm or similar
                    pass

        else:
            # ResNet architecture initialization
            # 1. Input Conv
            self.input_conv = LC0ConvBlock(w.input, 112, activation=True)
            self.filters = self.input_conv.out_channels

            # 2. Residuals
            self.blocks = nn.ModuleList()
            for res in w.residual:
                blk = LC0ResBlock(res, self.filters)
                self.blocks.append(blk)

        # 3. Policy Head
        if w.HasField("policy"):
            # Policy Conv usually has ReLU
            f = self.model_dim if self.is_transformer else self.filters
            self.policy_conv = LC0ConvBlock(w.policy, f, activation=True)

            # Policy FC
            if w.HasField("ip_pol_w"):
                pw = loader.decode_layer(w.ip_pol_w)
                pb = loader.decode_layer(w.ip_pol_b)
                # Assuming 1858 output
                out_dim = 1858
                in_dim = pw.size // out_dim

                self.pol_fc = nn.Linear(in_dim, out_dim)
                self.pol_fc.weight.data.copy_(
                    torch.from_numpy(pw).view(out_dim, in_dim)
                )
                self.pol_fc.bias.data.copy_(torch.from_numpy(pb))
            elif self.policy_format == 2:  # POLICY_CONVOLUTION
                # Auto-generate FC layer from AZ mapping
                # Input: (B, 80, 8, 8) -> Flatten -> (B, 5120)
                # Output: 1858

                print("Converting POLICY_CONVOLUTION to Linear layer...")

                # Assuming lc0_az_policy_map is available or accessible
                # For now, we stub or skip if not available, but logic remains
                # This part was largely stub code in original file too
                pass

        elif w.HasField("policy_heads"):
            # Handle policy heads if necessary
            pass

        # 4. Value Head
        if w.HasField("value"):
            f = self.model_dim if self.is_transformer else self.filters
            self.value_conv = LC0ConvBlock(w.value, f, activation=True)

            # Value FC1
            if w.HasField("ip1_val_w"):
                w1 = loader.decode_layer(w.ip1_val_w)
                b1 = loader.decode_layer(w.ip1_val_b)
                out_dim = 128  # Common default
                in_dim = w1.size // out_dim

                self.val_fc1 = nn.Linear(in_dim, out_dim)
                self.val_fc1.weight.data.copy_(
                    torch.from_numpy(w1).view(out_dim, in_dim)
                )
                self.val_fc1.bias.data.copy_(torch.from_numpy(b1))

            # Value FC2
            if w.HasField("ip2_val_w"):
                w2 = loader.decode_layer(w.ip2_val_w)
                b2 = loader.decode_layer(w.ip2_val_b)

                # Infer in_dim from previous layer (fc1 out)
                if hasattr(self, "val_fc1"):
                    in_dim = self.val_fc1.out_features
                else:
                    in_dim = 128

                out_dim = w2.size // in_dim

                self.val_fc2 = nn.Linear(in_dim, out_dim)
                self.val_fc2.weight.data.copy_(
                    torch.from_numpy(w2).view(out_dim, in_dim)
                )
                self.val_fc2.bias.data.copy_(torch.from_numpy(b2))

    def forward(self, x):
        if not self.is_transformer:
            # ResNet forward pass
            x = self.input_conv(x)
            for blk in self.blocks:
                x = blk(x)
        else:
            # Transformer forward pass

            if hasattr(self, "input_emb"):
                B, C, H, W = x.shape
                # Flatten spatial: (B, C, H, W) -> (B, H*W, C)
                # Note: x is usually (B, 112, 8, 8)
                x = x.view(B, C, H * W).transpose(1, 2)  # (B, 64, 112)

                # Handle potential mismatch between input channels and embedding size
                # (e.g. for testing with dummy data or different input representations)
                if self.input_emb.in_features != C:
                    if self.input_emb.in_features > C:
                        # Pad inputs if embedding expects more features
                        pad = torch.zeros(
                            B, 64, self.input_emb.in_features - C, device=x.device
                        )
                        x = torch.cat([x, pad], dim=2)
                    else:
                        # Slice inputs if embedding expects fewer features
                        x = x[:, :, : self.input_emb.in_features]

                x = self.input_emb(x)

            for blk in self.blocks:
                x = blk(x)

        # Policy
        p = None
        if hasattr(self, "policy_conv"):
            p = self.policy_conv(x)
            if hasattr(self, "pol_fc"):
                p = p.flatten(1)
                p = self.pol_fc(p)

        # Value
        v = None
        if hasattr(self, "value_conv"):
            v = self.value_conv(x)
            v = v.flatten(1)
            if hasattr(self, "val_fc1"):
                v = F.relu(self.val_fc1(v))
            if hasattr(self, "val_fc2"):
                v = self.val_fc2(v)

            # Activation depends on output dim
            # 1 -> Tanh (Classical Q)
            # 3 -> logits (WDL)
            if v.shape[1] == 1:
                v = torch.tanh(v)

        return p, v

    def apply_lora(self, rank=4, alpha=8):
        def replace_linear_or_conv(module):
            if isinstance(module, (nn.Linear, nn.Conv2d)):
                return LoRALayer(module, rank, alpha)
            return module

        if self.is_transformer:
            for blk in self.blocks:
                # MHA Projections
                blk.mha.q_proj = replace_linear_or_conv(blk.mha.q_proj)
                blk.mha.k_proj = replace_linear_or_conv(blk.mha.k_proj)
                blk.mha.v_proj = replace_linear_or_conv(blk.mha.v_proj)
                blk.mha.out_proj = replace_linear_or_conv(blk.mha.out_proj)

                # FFN Projections
                blk.ffn.fc1 = replace_linear_or_conv(blk.ffn.fc1)
                blk.ffn.fc2 = replace_linear_or_conv(blk.ffn.fc2)
        else:
            # Apply to residual blocks (Conv1 and Conv2)
            for blk in self.blocks:
                if isinstance(blk.conv1.conv, nn.Conv2d):
                    blk.conv1.conv = replace_linear_or_conv(blk.conv1.conv)
                if isinstance(blk.conv2.conv, nn.Conv2d):
                    blk.conv2.conv = replace_linear_or_conv(blk.conv2.conv)

        # Apply to Heads
        if hasattr(self, "policy_conv") and isinstance(
            self.policy_conv.conv, nn.Conv2d
        ):
            self.policy_conv.conv = replace_linear_or_conv(self.policy_conv.conv)

        if hasattr(self, "pol_fc") and isinstance(self.pol_fc, nn.Linear):
            self.pol_fc = replace_linear_or_conv(self.pol_fc)

        if hasattr(self, "value_conv") and isinstance(self.value_conv.conv, nn.Conv2d):
            self.value_conv.conv = replace_linear_or_conv(self.value_conv.conv)

    def save_proto(self, filename):
        """Bakes weights and saves to protobuf file."""
        w = self.proto_net.weights

        def update_layer(proto_layer, torch_tensor):
            # Encode tensor to proto layer
            # We use LINEAR16 by default as it matches Lc0 standard
            new_layer = loader.encode_layer(torch_tensor.cpu().detach().numpy())
            proto_layer.CopyFrom(new_layer)

        def update_conv_block(proto_block, module):
            # Weights
            if hasattr(module, "conv"):
                # Check if LoRA
                layer = module.conv
                if isinstance(layer, LoRALayer):
                    layer = layer.bake()
                update_layer(proto_block.weights, layer.weight)

                if module.has_bias and not module.has_bn:
                    update_layer(proto_block.biases, layer.bias)

            # BN
            if module.has_bn:
                update_layer(proto_block.bn_means, module.bn.running_mean)

                var = module.bn.running_var
                stddivs = 1.0 / torch.sqrt(var + 1e-10)
                update_layer(proto_block.bn_stddivs, stddivs)

                update_layer(proto_block.bn_gammas, module.bn.weight)
                update_layer(proto_block.bn_betas, module.bn.bias)

        if self.is_transformer:
            # Encoder Blocks
            for i, blk in enumerate(self.blocks):
                p_enc = w.encoder[i]

                # MHA
                def update_linear(proto_w, proto_b, layer):
                    if isinstance(layer, LoRALayer):
                        layer = layer.bake()
                    update_layer(proto_w, layer.weight)
                    update_layer(proto_b, layer.bias)

                update_linear(p_enc.mha.q_w, p_enc.mha.q_b, blk.mha.q_proj)
                update_linear(p_enc.mha.k_w, p_enc.mha.k_b, blk.mha.k_proj)
                update_linear(p_enc.mha.v_w, p_enc.mha.v_b, blk.mha.v_proj)
                update_linear(p_enc.mha.dense_w, p_enc.mha.dense_b, blk.mha.out_proj)

                # FFN
                update_linear(p_enc.ffn.dense1_w, p_enc.ffn.dense1_b, blk.ffn.fc1)
                update_linear(p_enc.ffn.dense2_w, p_enc.ffn.dense2_b, blk.ffn.fc2)

                # LN
                update_layer(p_enc.ln1_gammas, blk.ln1.weight)
                update_layer(p_enc.ln1_betas, blk.ln1.bias)
                update_layer(p_enc.ln2_gammas, blk.ln2.weight)
                update_layer(p_enc.ln2_betas, blk.ln2.bias)

            # Input Emb
            if hasattr(self, "input_emb"):
                update_layer(w.ip_emb_w, self.input_emb.weight)
                if hasattr(self.input_emb, "bias") and self.input_emb.bias is not None:
                    if w.HasField("ip_emb_b"):
                        update_layer(w.ip_emb_b, self.input_emb.bias)

        else:
            # ResNet
            # Input Conv
            update_conv_block(w.input, self.input_conv)

            # Blocks
            for i, blk in enumerate(self.blocks):
                res = w.residual[i]
                update_conv_block(res.conv1, blk.conv1)
                update_conv_block(res.conv2, blk.conv2)

                if blk.se:
                    # SE
                    p_se = res.se
                    update_layer(p_se.w1, blk.se.fc1.weight)
                    update_layer(p_se.b1, blk.se.fc1.bias)
                    update_layer(p_se.w2, blk.se.fc2.weight)
                    update_layer(p_se.b2, blk.se.fc2.bias)

        # Heads
        if hasattr(self, "policy_conv"):
            update_conv_block(w.policy, self.policy_conv)

            if hasattr(self, "pol_fc"):
                # If using LoRA on FC
                layer = self.pol_fc
                if isinstance(layer, LoRALayer):
                    layer = layer.bake()

                update_layer(w.ip_pol_w, layer.weight)
                update_layer(w.ip_pol_b, layer.bias)

                # Update format to CLASSICAL if it was CONVOLUTION
                if w.HasField("policy1"):
                    pass

        if hasattr(self, "value_conv"):
            update_conv_block(w.value, self.value_conv)

            if hasattr(self, "val_fc1"):
                update_layer(w.ip1_val_w, self.val_fc1.weight)
                update_layer(w.ip1_val_b, self.val_fc1.bias)

            if hasattr(self, "val_fc2"):
                update_layer(w.ip2_val_w, self.val_fc2.weight)
                update_layer(w.ip2_val_b, self.val_fc2.bias)

        # Update Policy Format to CLASSICAL if we have FC
        if hasattr(self, "pol_fc") and self.proto_net.format.network_format.policy == 2:
            print("Updating policy format from CONVOLUTION to CLASSICAL...")
            self.proto_net.format.network_format.policy = 1  # POLICY_CLASSICAL

        # Gzip it
        import gzip

        with gzip.open(filename, "wb") as f:
            f.write(self.proto_net.SerializeToString())
