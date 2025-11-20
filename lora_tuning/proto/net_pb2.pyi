from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class EngineVersion(_message.Message):
    __slots__ = ("major", "minor", "patch")
    MAJOR_FIELD_NUMBER: _ClassVar[int]
    MINOR_FIELD_NUMBER: _ClassVar[int]
    PATCH_FIELD_NUMBER: _ClassVar[int]
    major: int
    minor: int
    patch: int
    def __init__(self, major: _Optional[int] = ..., minor: _Optional[int] = ..., patch: _Optional[int] = ...) -> None: ...

class Weights(_message.Message):
    __slots__ = ("input", "residual", "ip_emb_preproc_w", "ip_emb_preproc_b", "ip_emb_w", "ip_emb_b", "ip_emb_ln_gammas", "ip_emb_ln_betas", "ip_mult_gate", "ip_add_gate", "ip_emb_ffn", "ip_emb_ffn_ln_gammas", "ip_emb_ffn_ln_betas", "encoder", "headcount", "pol_encoder", "pol_headcount", "policy1", "policy", "ip_pol_w", "ip_pol_b", "ip2_pol_w", "ip2_pol_b", "ip3_pol_w", "ip3_pol_b", "ip4_pol_w", "value", "ip_val_w", "ip_val_b", "ip1_val_w", "ip1_val_b", "ip2_val_w", "ip2_val_b", "value_heads", "policy_heads", "moves_left", "ip_mov_w", "ip_mov_b", "ip1_mov_w", "ip1_mov_b", "ip2_mov_w", "ip2_mov_b", "smolgen_w", "smolgen_b")
    class Layer(_message.Message):
        __slots__ = ("min_val", "max_val", "params", "encoding", "dims")
        class Encoding(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
            __slots__ = ()
            UNKNOWN_ENCODING: _ClassVar[Weights.Layer.Encoding]
            LINEAR16: _ClassVar[Weights.Layer.Encoding]
            FLOAT16: _ClassVar[Weights.Layer.Encoding]
            BFLOAT16: _ClassVar[Weights.Layer.Encoding]
        UNKNOWN_ENCODING: Weights.Layer.Encoding
        LINEAR16: Weights.Layer.Encoding
        FLOAT16: Weights.Layer.Encoding
        BFLOAT16: Weights.Layer.Encoding
        MIN_VAL_FIELD_NUMBER: _ClassVar[int]
        MAX_VAL_FIELD_NUMBER: _ClassVar[int]
        PARAMS_FIELD_NUMBER: _ClassVar[int]
        ENCODING_FIELD_NUMBER: _ClassVar[int]
        DIMS_FIELD_NUMBER: _ClassVar[int]
        min_val: float
        max_val: float
        params: bytes
        encoding: Weights.Layer.Encoding
        dims: _containers.RepeatedScalarFieldContainer[int]
        def __init__(self, min_val: _Optional[float] = ..., max_val: _Optional[float] = ..., params: _Optional[bytes] = ..., encoding: _Optional[_Union[Weights.Layer.Encoding, str]] = ..., dims: _Optional[_Iterable[int]] = ...) -> None: ...
    class ConvBlock(_message.Message):
        __slots__ = ("weights", "biases", "bn_means", "bn_stddivs", "bn_gammas", "bn_betas")
        WEIGHTS_FIELD_NUMBER: _ClassVar[int]
        BIASES_FIELD_NUMBER: _ClassVar[int]
        BN_MEANS_FIELD_NUMBER: _ClassVar[int]
        BN_STDDIVS_FIELD_NUMBER: _ClassVar[int]
        BN_GAMMAS_FIELD_NUMBER: _ClassVar[int]
        BN_BETAS_FIELD_NUMBER: _ClassVar[int]
        weights: Weights.Layer
        biases: Weights.Layer
        bn_means: Weights.Layer
        bn_stddivs: Weights.Layer
        bn_gammas: Weights.Layer
        bn_betas: Weights.Layer
        def __init__(self, weights: _Optional[_Union[Weights.Layer, _Mapping]] = ..., biases: _Optional[_Union[Weights.Layer, _Mapping]] = ..., bn_means: _Optional[_Union[Weights.Layer, _Mapping]] = ..., bn_stddivs: _Optional[_Union[Weights.Layer, _Mapping]] = ..., bn_gammas: _Optional[_Union[Weights.Layer, _Mapping]] = ..., bn_betas: _Optional[_Union[Weights.Layer, _Mapping]] = ...) -> None: ...
    class SEunit(_message.Message):
        __slots__ = ("w1", "b1", "w2", "b2")
        W1_FIELD_NUMBER: _ClassVar[int]
        B1_FIELD_NUMBER: _ClassVar[int]
        W2_FIELD_NUMBER: _ClassVar[int]
        B2_FIELD_NUMBER: _ClassVar[int]
        w1: Weights.Layer
        b1: Weights.Layer
        w2: Weights.Layer
        b2: Weights.Layer
        def __init__(self, w1: _Optional[_Union[Weights.Layer, _Mapping]] = ..., b1: _Optional[_Union[Weights.Layer, _Mapping]] = ..., w2: _Optional[_Union[Weights.Layer, _Mapping]] = ..., b2: _Optional[_Union[Weights.Layer, _Mapping]] = ...) -> None: ...
    class Residual(_message.Message):
        __slots__ = ("conv1", "conv2", "se")
        CONV1_FIELD_NUMBER: _ClassVar[int]
        CONV2_FIELD_NUMBER: _ClassVar[int]
        SE_FIELD_NUMBER: _ClassVar[int]
        conv1: Weights.ConvBlock
        conv2: Weights.ConvBlock
        se: Weights.SEunit
        def __init__(self, conv1: _Optional[_Union[Weights.ConvBlock, _Mapping]] = ..., conv2: _Optional[_Union[Weights.ConvBlock, _Mapping]] = ..., se: _Optional[_Union[Weights.SEunit, _Mapping]] = ...) -> None: ...
    class Smolgen(_message.Message):
        __slots__ = ("compress", "dense1_w", "dense1_b", "ln1_gammas", "ln1_betas", "dense2_w", "dense2_b", "ln2_gammas", "ln2_betas")
        COMPRESS_FIELD_NUMBER: _ClassVar[int]
        DENSE1_W_FIELD_NUMBER: _ClassVar[int]
        DENSE1_B_FIELD_NUMBER: _ClassVar[int]
        LN1_GAMMAS_FIELD_NUMBER: _ClassVar[int]
        LN1_BETAS_FIELD_NUMBER: _ClassVar[int]
        DENSE2_W_FIELD_NUMBER: _ClassVar[int]
        DENSE2_B_FIELD_NUMBER: _ClassVar[int]
        LN2_GAMMAS_FIELD_NUMBER: _ClassVar[int]
        LN2_BETAS_FIELD_NUMBER: _ClassVar[int]
        compress: Weights.Layer
        dense1_w: Weights.Layer
        dense1_b: Weights.Layer
        ln1_gammas: Weights.Layer
        ln1_betas: Weights.Layer
        dense2_w: Weights.Layer
        dense2_b: Weights.Layer
        ln2_gammas: Weights.Layer
        ln2_betas: Weights.Layer
        def __init__(self, compress: _Optional[_Union[Weights.Layer, _Mapping]] = ..., dense1_w: _Optional[_Union[Weights.Layer, _Mapping]] = ..., dense1_b: _Optional[_Union[Weights.Layer, _Mapping]] = ..., ln1_gammas: _Optional[_Union[Weights.Layer, _Mapping]] = ..., ln1_betas: _Optional[_Union[Weights.Layer, _Mapping]] = ..., dense2_w: _Optional[_Union[Weights.Layer, _Mapping]] = ..., dense2_b: _Optional[_Union[Weights.Layer, _Mapping]] = ..., ln2_gammas: _Optional[_Union[Weights.Layer, _Mapping]] = ..., ln2_betas: _Optional[_Union[Weights.Layer, _Mapping]] = ...) -> None: ...
    class MHA(_message.Message):
        __slots__ = ("q_w", "q_b", "k_w", "k_b", "v_w", "v_b", "dense_w", "dense_b", "smolgen", "rpe_q", "rpe_k", "rpe_v")
        Q_W_FIELD_NUMBER: _ClassVar[int]
        Q_B_FIELD_NUMBER: _ClassVar[int]
        K_W_FIELD_NUMBER: _ClassVar[int]
        K_B_FIELD_NUMBER: _ClassVar[int]
        V_W_FIELD_NUMBER: _ClassVar[int]
        V_B_FIELD_NUMBER: _ClassVar[int]
        DENSE_W_FIELD_NUMBER: _ClassVar[int]
        DENSE_B_FIELD_NUMBER: _ClassVar[int]
        SMOLGEN_FIELD_NUMBER: _ClassVar[int]
        RPE_Q_FIELD_NUMBER: _ClassVar[int]
        RPE_K_FIELD_NUMBER: _ClassVar[int]
        RPE_V_FIELD_NUMBER: _ClassVar[int]
        q_w: Weights.Layer
        q_b: Weights.Layer
        k_w: Weights.Layer
        k_b: Weights.Layer
        v_w: Weights.Layer
        v_b: Weights.Layer
        dense_w: Weights.Layer
        dense_b: Weights.Layer
        smolgen: Weights.Smolgen
        rpe_q: Weights.Layer
        rpe_k: Weights.Layer
        rpe_v: Weights.Layer
        def __init__(self, q_w: _Optional[_Union[Weights.Layer, _Mapping]] = ..., q_b: _Optional[_Union[Weights.Layer, _Mapping]] = ..., k_w: _Optional[_Union[Weights.Layer, _Mapping]] = ..., k_b: _Optional[_Union[Weights.Layer, _Mapping]] = ..., v_w: _Optional[_Union[Weights.Layer, _Mapping]] = ..., v_b: _Optional[_Union[Weights.Layer, _Mapping]] = ..., dense_w: _Optional[_Union[Weights.Layer, _Mapping]] = ..., dense_b: _Optional[_Union[Weights.Layer, _Mapping]] = ..., smolgen: _Optional[_Union[Weights.Smolgen, _Mapping]] = ..., rpe_q: _Optional[_Union[Weights.Layer, _Mapping]] = ..., rpe_k: _Optional[_Union[Weights.Layer, _Mapping]] = ..., rpe_v: _Optional[_Union[Weights.Layer, _Mapping]] = ...) -> None: ...
    class FFN(_message.Message):
        __slots__ = ("dense1_w", "dense1_b", "dense2_w", "dense2_b")
        DENSE1_W_FIELD_NUMBER: _ClassVar[int]
        DENSE1_B_FIELD_NUMBER: _ClassVar[int]
        DENSE2_W_FIELD_NUMBER: _ClassVar[int]
        DENSE2_B_FIELD_NUMBER: _ClassVar[int]
        dense1_w: Weights.Layer
        dense1_b: Weights.Layer
        dense2_w: Weights.Layer
        dense2_b: Weights.Layer
        def __init__(self, dense1_w: _Optional[_Union[Weights.Layer, _Mapping]] = ..., dense1_b: _Optional[_Union[Weights.Layer, _Mapping]] = ..., dense2_w: _Optional[_Union[Weights.Layer, _Mapping]] = ..., dense2_b: _Optional[_Union[Weights.Layer, _Mapping]] = ...) -> None: ...
    class EncoderLayer(_message.Message):
        __slots__ = ("mha", "ln1_gammas", "ln1_betas", "ffn", "ln2_gammas", "ln2_betas")
        MHA_FIELD_NUMBER: _ClassVar[int]
        LN1_GAMMAS_FIELD_NUMBER: _ClassVar[int]
        LN1_BETAS_FIELD_NUMBER: _ClassVar[int]
        FFN_FIELD_NUMBER: _ClassVar[int]
        LN2_GAMMAS_FIELD_NUMBER: _ClassVar[int]
        LN2_BETAS_FIELD_NUMBER: _ClassVar[int]
        mha: Weights.MHA
        ln1_gammas: Weights.Layer
        ln1_betas: Weights.Layer
        ffn: Weights.FFN
        ln2_gammas: Weights.Layer
        ln2_betas: Weights.Layer
        def __init__(self, mha: _Optional[_Union[Weights.MHA, _Mapping]] = ..., ln1_gammas: _Optional[_Union[Weights.Layer, _Mapping]] = ..., ln1_betas: _Optional[_Union[Weights.Layer, _Mapping]] = ..., ffn: _Optional[_Union[Weights.FFN, _Mapping]] = ..., ln2_gammas: _Optional[_Union[Weights.Layer, _Mapping]] = ..., ln2_betas: _Optional[_Union[Weights.Layer, _Mapping]] = ...) -> None: ...
    class PolicyHead(_message.Message):
        __slots__ = ("ip_pol_w", "ip_pol_b", "ip2_pol_w", "ip2_pol_b", "ip3_pol_w", "ip3_pol_b", "ip4_pol_w", "pol_encoder", "pol_headcount", "policy1", "policy")
        IP_POL_W_FIELD_NUMBER: _ClassVar[int]
        IP_POL_B_FIELD_NUMBER: _ClassVar[int]
        IP2_POL_W_FIELD_NUMBER: _ClassVar[int]
        IP2_POL_B_FIELD_NUMBER: _ClassVar[int]
        IP3_POL_W_FIELD_NUMBER: _ClassVar[int]
        IP3_POL_B_FIELD_NUMBER: _ClassVar[int]
        IP4_POL_W_FIELD_NUMBER: _ClassVar[int]
        POL_ENCODER_FIELD_NUMBER: _ClassVar[int]
        POL_HEADCOUNT_FIELD_NUMBER: _ClassVar[int]
        POLICY1_FIELD_NUMBER: _ClassVar[int]
        POLICY_FIELD_NUMBER: _ClassVar[int]
        ip_pol_w: Weights.Layer
        ip_pol_b: Weights.Layer
        ip2_pol_w: Weights.Layer
        ip2_pol_b: Weights.Layer
        ip3_pol_w: Weights.Layer
        ip3_pol_b: Weights.Layer
        ip4_pol_w: Weights.Layer
        pol_encoder: _containers.RepeatedCompositeFieldContainer[Weights.EncoderLayer]
        pol_headcount: int
        policy1: Weights.ConvBlock
        policy: Weights.ConvBlock
        def __init__(self, ip_pol_w: _Optional[_Union[Weights.Layer, _Mapping]] = ..., ip_pol_b: _Optional[_Union[Weights.Layer, _Mapping]] = ..., ip2_pol_w: _Optional[_Union[Weights.Layer, _Mapping]] = ..., ip2_pol_b: _Optional[_Union[Weights.Layer, _Mapping]] = ..., ip3_pol_w: _Optional[_Union[Weights.Layer, _Mapping]] = ..., ip3_pol_b: _Optional[_Union[Weights.Layer, _Mapping]] = ..., ip4_pol_w: _Optional[_Union[Weights.Layer, _Mapping]] = ..., pol_encoder: _Optional[_Iterable[_Union[Weights.EncoderLayer, _Mapping]]] = ..., pol_headcount: _Optional[int] = ..., policy1: _Optional[_Union[Weights.ConvBlock, _Mapping]] = ..., policy: _Optional[_Union[Weights.ConvBlock, _Mapping]] = ...) -> None: ...
    class ValueHead(_message.Message):
        __slots__ = ("ip_val_w", "ip_val_b", "ip1_val_w", "ip1_val_b", "ip2_val_w", "ip2_val_b", "ip_val_err_w", "ip_val_err_b", "ip_val_cat_w", "ip_val_cat_b", "value")
        IP_VAL_W_FIELD_NUMBER: _ClassVar[int]
        IP_VAL_B_FIELD_NUMBER: _ClassVar[int]
        IP1_VAL_W_FIELD_NUMBER: _ClassVar[int]
        IP1_VAL_B_FIELD_NUMBER: _ClassVar[int]
        IP2_VAL_W_FIELD_NUMBER: _ClassVar[int]
        IP2_VAL_B_FIELD_NUMBER: _ClassVar[int]
        IP_VAL_ERR_W_FIELD_NUMBER: _ClassVar[int]
        IP_VAL_ERR_B_FIELD_NUMBER: _ClassVar[int]
        IP_VAL_CAT_W_FIELD_NUMBER: _ClassVar[int]
        IP_VAL_CAT_B_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        ip_val_w: Weights.Layer
        ip_val_b: Weights.Layer
        ip1_val_w: Weights.Layer
        ip1_val_b: Weights.Layer
        ip2_val_w: Weights.Layer
        ip2_val_b: Weights.Layer
        ip_val_err_w: Weights.Layer
        ip_val_err_b: Weights.Layer
        ip_val_cat_w: Weights.Layer
        ip_val_cat_b: Weights.Layer
        value: Weights.ConvBlock
        def __init__(self, ip_val_w: _Optional[_Union[Weights.Layer, _Mapping]] = ..., ip_val_b: _Optional[_Union[Weights.Layer, _Mapping]] = ..., ip1_val_w: _Optional[_Union[Weights.Layer, _Mapping]] = ..., ip1_val_b: _Optional[_Union[Weights.Layer, _Mapping]] = ..., ip2_val_w: _Optional[_Union[Weights.Layer, _Mapping]] = ..., ip2_val_b: _Optional[_Union[Weights.Layer, _Mapping]] = ..., ip_val_err_w: _Optional[_Union[Weights.Layer, _Mapping]] = ..., ip_val_err_b: _Optional[_Union[Weights.Layer, _Mapping]] = ..., ip_val_cat_w: _Optional[_Union[Weights.Layer, _Mapping]] = ..., ip_val_cat_b: _Optional[_Union[Weights.Layer, _Mapping]] = ..., value: _Optional[_Union[Weights.ConvBlock, _Mapping]] = ...) -> None: ...
    class PolicyHeadMap(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: Weights.PolicyHead
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[Weights.PolicyHead, _Mapping]] = ...) -> None: ...
    class PolicyHeads(_message.Message):
        __slots__ = ("ip_pol_w", "ip_pol_b", "vanilla", "optimistic_st", "soft", "opponent", "policy_head_map")
        IP_POL_W_FIELD_NUMBER: _ClassVar[int]
        IP_POL_B_FIELD_NUMBER: _ClassVar[int]
        VANILLA_FIELD_NUMBER: _ClassVar[int]
        OPTIMISTIC_ST_FIELD_NUMBER: _ClassVar[int]
        SOFT_FIELD_NUMBER: _ClassVar[int]
        OPPONENT_FIELD_NUMBER: _ClassVar[int]
        POLICY_HEAD_MAP_FIELD_NUMBER: _ClassVar[int]
        ip_pol_w: Weights.Layer
        ip_pol_b: Weights.Layer
        vanilla: Weights.PolicyHead
        optimistic_st: Weights.PolicyHead
        soft: Weights.PolicyHead
        opponent: Weights.PolicyHead
        policy_head_map: _containers.RepeatedCompositeFieldContainer[Weights.PolicyHeadMap]
        def __init__(self, ip_pol_w: _Optional[_Union[Weights.Layer, _Mapping]] = ..., ip_pol_b: _Optional[_Union[Weights.Layer, _Mapping]] = ..., vanilla: _Optional[_Union[Weights.PolicyHead, _Mapping]] = ..., optimistic_st: _Optional[_Union[Weights.PolicyHead, _Mapping]] = ..., soft: _Optional[_Union[Weights.PolicyHead, _Mapping]] = ..., opponent: _Optional[_Union[Weights.PolicyHead, _Mapping]] = ..., policy_head_map: _Optional[_Iterable[_Union[Weights.PolicyHeadMap, _Mapping]]] = ...) -> None: ...
    class ValueHeadMap(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: Weights.ValueHead
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[Weights.ValueHead, _Mapping]] = ...) -> None: ...
    class ValueHeads(_message.Message):
        __slots__ = ("winner", "q", "st", "value_head_map")
        WINNER_FIELD_NUMBER: _ClassVar[int]
        Q_FIELD_NUMBER: _ClassVar[int]
        ST_FIELD_NUMBER: _ClassVar[int]
        VALUE_HEAD_MAP_FIELD_NUMBER: _ClassVar[int]
        winner: Weights.ValueHead
        q: Weights.ValueHead
        st: Weights.ValueHead
        value_head_map: _containers.RepeatedCompositeFieldContainer[Weights.ValueHeadMap]
        def __init__(self, winner: _Optional[_Union[Weights.ValueHead, _Mapping]] = ..., q: _Optional[_Union[Weights.ValueHead, _Mapping]] = ..., st: _Optional[_Union[Weights.ValueHead, _Mapping]] = ..., value_head_map: _Optional[_Iterable[_Union[Weights.ValueHeadMap, _Mapping]]] = ...) -> None: ...
    INPUT_FIELD_NUMBER: _ClassVar[int]
    RESIDUAL_FIELD_NUMBER: _ClassVar[int]
    IP_EMB_PREPROC_W_FIELD_NUMBER: _ClassVar[int]
    IP_EMB_PREPROC_B_FIELD_NUMBER: _ClassVar[int]
    IP_EMB_W_FIELD_NUMBER: _ClassVar[int]
    IP_EMB_B_FIELD_NUMBER: _ClassVar[int]
    IP_EMB_LN_GAMMAS_FIELD_NUMBER: _ClassVar[int]
    IP_EMB_LN_BETAS_FIELD_NUMBER: _ClassVar[int]
    IP_MULT_GATE_FIELD_NUMBER: _ClassVar[int]
    IP_ADD_GATE_FIELD_NUMBER: _ClassVar[int]
    IP_EMB_FFN_FIELD_NUMBER: _ClassVar[int]
    IP_EMB_FFN_LN_GAMMAS_FIELD_NUMBER: _ClassVar[int]
    IP_EMB_FFN_LN_BETAS_FIELD_NUMBER: _ClassVar[int]
    ENCODER_FIELD_NUMBER: _ClassVar[int]
    HEADCOUNT_FIELD_NUMBER: _ClassVar[int]
    POL_ENCODER_FIELD_NUMBER: _ClassVar[int]
    POL_HEADCOUNT_FIELD_NUMBER: _ClassVar[int]
    POLICY1_FIELD_NUMBER: _ClassVar[int]
    POLICY_FIELD_NUMBER: _ClassVar[int]
    IP_POL_W_FIELD_NUMBER: _ClassVar[int]
    IP_POL_B_FIELD_NUMBER: _ClassVar[int]
    IP2_POL_W_FIELD_NUMBER: _ClassVar[int]
    IP2_POL_B_FIELD_NUMBER: _ClassVar[int]
    IP3_POL_W_FIELD_NUMBER: _ClassVar[int]
    IP3_POL_B_FIELD_NUMBER: _ClassVar[int]
    IP4_POL_W_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    IP_VAL_W_FIELD_NUMBER: _ClassVar[int]
    IP_VAL_B_FIELD_NUMBER: _ClassVar[int]
    IP1_VAL_W_FIELD_NUMBER: _ClassVar[int]
    IP1_VAL_B_FIELD_NUMBER: _ClassVar[int]
    IP2_VAL_W_FIELD_NUMBER: _ClassVar[int]
    IP2_VAL_B_FIELD_NUMBER: _ClassVar[int]
    VALUE_HEADS_FIELD_NUMBER: _ClassVar[int]
    POLICY_HEADS_FIELD_NUMBER: _ClassVar[int]
    MOVES_LEFT_FIELD_NUMBER: _ClassVar[int]
    IP_MOV_W_FIELD_NUMBER: _ClassVar[int]
    IP_MOV_B_FIELD_NUMBER: _ClassVar[int]
    IP1_MOV_W_FIELD_NUMBER: _ClassVar[int]
    IP1_MOV_B_FIELD_NUMBER: _ClassVar[int]
    IP2_MOV_W_FIELD_NUMBER: _ClassVar[int]
    IP2_MOV_B_FIELD_NUMBER: _ClassVar[int]
    SMOLGEN_W_FIELD_NUMBER: _ClassVar[int]
    SMOLGEN_B_FIELD_NUMBER: _ClassVar[int]
    input: Weights.ConvBlock
    residual: _containers.RepeatedCompositeFieldContainer[Weights.Residual]
    ip_emb_preproc_w: Weights.Layer
    ip_emb_preproc_b: Weights.Layer
    ip_emb_w: Weights.Layer
    ip_emb_b: Weights.Layer
    ip_emb_ln_gammas: Weights.Layer
    ip_emb_ln_betas: Weights.Layer
    ip_mult_gate: Weights.Layer
    ip_add_gate: Weights.Layer
    ip_emb_ffn: Weights.FFN
    ip_emb_ffn_ln_gammas: Weights.Layer
    ip_emb_ffn_ln_betas: Weights.Layer
    encoder: _containers.RepeatedCompositeFieldContainer[Weights.EncoderLayer]
    headcount: int
    pol_encoder: _containers.RepeatedCompositeFieldContainer[Weights.EncoderLayer]
    pol_headcount: int
    policy1: Weights.ConvBlock
    policy: Weights.ConvBlock
    ip_pol_w: Weights.Layer
    ip_pol_b: Weights.Layer
    ip2_pol_w: Weights.Layer
    ip2_pol_b: Weights.Layer
    ip3_pol_w: Weights.Layer
    ip3_pol_b: Weights.Layer
    ip4_pol_w: Weights.Layer
    value: Weights.ConvBlock
    ip_val_w: Weights.Layer
    ip_val_b: Weights.Layer
    ip1_val_w: Weights.Layer
    ip1_val_b: Weights.Layer
    ip2_val_w: Weights.Layer
    ip2_val_b: Weights.Layer
    value_heads: Weights.ValueHeads
    policy_heads: Weights.PolicyHeads
    moves_left: Weights.ConvBlock
    ip_mov_w: Weights.Layer
    ip_mov_b: Weights.Layer
    ip1_mov_w: Weights.Layer
    ip1_mov_b: Weights.Layer
    ip2_mov_w: Weights.Layer
    ip2_mov_b: Weights.Layer
    smolgen_w: Weights.Layer
    smolgen_b: Weights.Layer
    def __init__(self, input: _Optional[_Union[Weights.ConvBlock, _Mapping]] = ..., residual: _Optional[_Iterable[_Union[Weights.Residual, _Mapping]]] = ..., ip_emb_preproc_w: _Optional[_Union[Weights.Layer, _Mapping]] = ..., ip_emb_preproc_b: _Optional[_Union[Weights.Layer, _Mapping]] = ..., ip_emb_w: _Optional[_Union[Weights.Layer, _Mapping]] = ..., ip_emb_b: _Optional[_Union[Weights.Layer, _Mapping]] = ..., ip_emb_ln_gammas: _Optional[_Union[Weights.Layer, _Mapping]] = ..., ip_emb_ln_betas: _Optional[_Union[Weights.Layer, _Mapping]] = ..., ip_mult_gate: _Optional[_Union[Weights.Layer, _Mapping]] = ..., ip_add_gate: _Optional[_Union[Weights.Layer, _Mapping]] = ..., ip_emb_ffn: _Optional[_Union[Weights.FFN, _Mapping]] = ..., ip_emb_ffn_ln_gammas: _Optional[_Union[Weights.Layer, _Mapping]] = ..., ip_emb_ffn_ln_betas: _Optional[_Union[Weights.Layer, _Mapping]] = ..., encoder: _Optional[_Iterable[_Union[Weights.EncoderLayer, _Mapping]]] = ..., headcount: _Optional[int] = ..., pol_encoder: _Optional[_Iterable[_Union[Weights.EncoderLayer, _Mapping]]] = ..., pol_headcount: _Optional[int] = ..., policy1: _Optional[_Union[Weights.ConvBlock, _Mapping]] = ..., policy: _Optional[_Union[Weights.ConvBlock, _Mapping]] = ..., ip_pol_w: _Optional[_Union[Weights.Layer, _Mapping]] = ..., ip_pol_b: _Optional[_Union[Weights.Layer, _Mapping]] = ..., ip2_pol_w: _Optional[_Union[Weights.Layer, _Mapping]] = ..., ip2_pol_b: _Optional[_Union[Weights.Layer, _Mapping]] = ..., ip3_pol_w: _Optional[_Union[Weights.Layer, _Mapping]] = ..., ip3_pol_b: _Optional[_Union[Weights.Layer, _Mapping]] = ..., ip4_pol_w: _Optional[_Union[Weights.Layer, _Mapping]] = ..., value: _Optional[_Union[Weights.ConvBlock, _Mapping]] = ..., ip_val_w: _Optional[_Union[Weights.Layer, _Mapping]] = ..., ip_val_b: _Optional[_Union[Weights.Layer, _Mapping]] = ..., ip1_val_w: _Optional[_Union[Weights.Layer, _Mapping]] = ..., ip1_val_b: _Optional[_Union[Weights.Layer, _Mapping]] = ..., ip2_val_w: _Optional[_Union[Weights.Layer, _Mapping]] = ..., ip2_val_b: _Optional[_Union[Weights.Layer, _Mapping]] = ..., value_heads: _Optional[_Union[Weights.ValueHeads, _Mapping]] = ..., policy_heads: _Optional[_Union[Weights.PolicyHeads, _Mapping]] = ..., moves_left: _Optional[_Union[Weights.ConvBlock, _Mapping]] = ..., ip_mov_w: _Optional[_Union[Weights.Layer, _Mapping]] = ..., ip_mov_b: _Optional[_Union[Weights.Layer, _Mapping]] = ..., ip1_mov_w: _Optional[_Union[Weights.Layer, _Mapping]] = ..., ip1_mov_b: _Optional[_Union[Weights.Layer, _Mapping]] = ..., ip2_mov_w: _Optional[_Union[Weights.Layer, _Mapping]] = ..., ip2_mov_b: _Optional[_Union[Weights.Layer, _Mapping]] = ..., smolgen_w: _Optional[_Union[Weights.Layer, _Mapping]] = ..., smolgen_b: _Optional[_Union[Weights.Layer, _Mapping]] = ...) -> None: ...

class TrainingParams(_message.Message):
    __slots__ = ("training_steps", "learning_rate", "mse_loss", "policy_loss", "accuracy", "lc0_params")
    TRAINING_STEPS_FIELD_NUMBER: _ClassVar[int]
    LEARNING_RATE_FIELD_NUMBER: _ClassVar[int]
    MSE_LOSS_FIELD_NUMBER: _ClassVar[int]
    POLICY_LOSS_FIELD_NUMBER: _ClassVar[int]
    ACCURACY_FIELD_NUMBER: _ClassVar[int]
    LC0_PARAMS_FIELD_NUMBER: _ClassVar[int]
    training_steps: int
    learning_rate: float
    mse_loss: float
    policy_loss: float
    accuracy: float
    lc0_params: str
    def __init__(self, training_steps: _Optional[int] = ..., learning_rate: _Optional[float] = ..., mse_loss: _Optional[float] = ..., policy_loss: _Optional[float] = ..., accuracy: _Optional[float] = ..., lc0_params: _Optional[str] = ...) -> None: ...

class NetworkFormat(_message.Message):
    __slots__ = ("input", "output", "network", "policy", "value", "moves_left", "default_activation", "smolgen_activation", "ffn_activation", "input_embedding")
    class InputFormat(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        INPUT_UNKNOWN: _ClassVar[NetworkFormat.InputFormat]
        INPUT_CLASSICAL_112_PLANE: _ClassVar[NetworkFormat.InputFormat]
        INPUT_112_WITH_CASTLING_PLANE: _ClassVar[NetworkFormat.InputFormat]
        INPUT_112_WITH_CANONICALIZATION: _ClassVar[NetworkFormat.InputFormat]
        INPUT_112_WITH_CANONICALIZATION_HECTOPLIES: _ClassVar[NetworkFormat.InputFormat]
        INPUT_112_WITH_CANONICALIZATION_HECTOPLIES_ARMAGEDDON: _ClassVar[NetworkFormat.InputFormat]
        INPUT_112_WITH_CANONICALIZATION_V2: _ClassVar[NetworkFormat.InputFormat]
        INPUT_112_WITH_CANONICALIZATION_V2_ARMAGEDDON: _ClassVar[NetworkFormat.InputFormat]
    INPUT_UNKNOWN: NetworkFormat.InputFormat
    INPUT_CLASSICAL_112_PLANE: NetworkFormat.InputFormat
    INPUT_112_WITH_CASTLING_PLANE: NetworkFormat.InputFormat
    INPUT_112_WITH_CANONICALIZATION: NetworkFormat.InputFormat
    INPUT_112_WITH_CANONICALIZATION_HECTOPLIES: NetworkFormat.InputFormat
    INPUT_112_WITH_CANONICALIZATION_HECTOPLIES_ARMAGEDDON: NetworkFormat.InputFormat
    INPUT_112_WITH_CANONICALIZATION_V2: NetworkFormat.InputFormat
    INPUT_112_WITH_CANONICALIZATION_V2_ARMAGEDDON: NetworkFormat.InputFormat
    class OutputFormat(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        OUTPUT_UNKNOWN: _ClassVar[NetworkFormat.OutputFormat]
        OUTPUT_CLASSICAL: _ClassVar[NetworkFormat.OutputFormat]
        OUTPUT_WDL: _ClassVar[NetworkFormat.OutputFormat]
    OUTPUT_UNKNOWN: NetworkFormat.OutputFormat
    OUTPUT_CLASSICAL: NetworkFormat.OutputFormat
    OUTPUT_WDL: NetworkFormat.OutputFormat
    class NetworkStructure(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        NETWORK_UNKNOWN: _ClassVar[NetworkFormat.NetworkStructure]
        NETWORK_CLASSICAL: _ClassVar[NetworkFormat.NetworkStructure]
        NETWORK_SE: _ClassVar[NetworkFormat.NetworkStructure]
        NETWORK_CLASSICAL_WITH_HEADFORMAT: _ClassVar[NetworkFormat.NetworkStructure]
        NETWORK_SE_WITH_HEADFORMAT: _ClassVar[NetworkFormat.NetworkStructure]
        NETWORK_ONNX: _ClassVar[NetworkFormat.NetworkStructure]
        NETWORK_ATTENTIONBODY_WITH_HEADFORMAT: _ClassVar[NetworkFormat.NetworkStructure]
        NETWORK_ATTENTIONBODY_WITH_MULTIHEADFORMAT: _ClassVar[NetworkFormat.NetworkStructure]
        NETWORK_AB_LEGACY_WITH_MULTIHEADFORMAT: _ClassVar[NetworkFormat.NetworkStructure]
    NETWORK_UNKNOWN: NetworkFormat.NetworkStructure
    NETWORK_CLASSICAL: NetworkFormat.NetworkStructure
    NETWORK_SE: NetworkFormat.NetworkStructure
    NETWORK_CLASSICAL_WITH_HEADFORMAT: NetworkFormat.NetworkStructure
    NETWORK_SE_WITH_HEADFORMAT: NetworkFormat.NetworkStructure
    NETWORK_ONNX: NetworkFormat.NetworkStructure
    NETWORK_ATTENTIONBODY_WITH_HEADFORMAT: NetworkFormat.NetworkStructure
    NETWORK_ATTENTIONBODY_WITH_MULTIHEADFORMAT: NetworkFormat.NetworkStructure
    NETWORK_AB_LEGACY_WITH_MULTIHEADFORMAT: NetworkFormat.NetworkStructure
    class PolicyFormat(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        POLICY_UNKNOWN: _ClassVar[NetworkFormat.PolicyFormat]
        POLICY_CLASSICAL: _ClassVar[NetworkFormat.PolicyFormat]
        POLICY_CONVOLUTION: _ClassVar[NetworkFormat.PolicyFormat]
        POLICY_ATTENTION: _ClassVar[NetworkFormat.PolicyFormat]
    POLICY_UNKNOWN: NetworkFormat.PolicyFormat
    POLICY_CLASSICAL: NetworkFormat.PolicyFormat
    POLICY_CONVOLUTION: NetworkFormat.PolicyFormat
    POLICY_ATTENTION: NetworkFormat.PolicyFormat
    class ValueFormat(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        VALUE_UNKNOWN: _ClassVar[NetworkFormat.ValueFormat]
        VALUE_CLASSICAL: _ClassVar[NetworkFormat.ValueFormat]
        VALUE_WDL: _ClassVar[NetworkFormat.ValueFormat]
        VALUE_PARAM: _ClassVar[NetworkFormat.ValueFormat]
    VALUE_UNKNOWN: NetworkFormat.ValueFormat
    VALUE_CLASSICAL: NetworkFormat.ValueFormat
    VALUE_WDL: NetworkFormat.ValueFormat
    VALUE_PARAM: NetworkFormat.ValueFormat
    class MovesLeftFormat(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        MOVES_LEFT_NONE: _ClassVar[NetworkFormat.MovesLeftFormat]
        MOVES_LEFT_V1: _ClassVar[NetworkFormat.MovesLeftFormat]
    MOVES_LEFT_NONE: NetworkFormat.MovesLeftFormat
    MOVES_LEFT_V1: NetworkFormat.MovesLeftFormat
    class ActivationFunction(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        ACTIVATION_DEFAULT: _ClassVar[NetworkFormat.ActivationFunction]
        ACTIVATION_MISH: _ClassVar[NetworkFormat.ActivationFunction]
        ACTIVATION_RELU: _ClassVar[NetworkFormat.ActivationFunction]
        ACTIVATION_NONE: _ClassVar[NetworkFormat.ActivationFunction]
        ACTIVATION_TANH: _ClassVar[NetworkFormat.ActivationFunction]
        ACTIVATION_SIGMOID: _ClassVar[NetworkFormat.ActivationFunction]
        ACTIVATION_SELU: _ClassVar[NetworkFormat.ActivationFunction]
        ACTIVATION_SWISH: _ClassVar[NetworkFormat.ActivationFunction]
        ACTIVATION_RELU_2: _ClassVar[NetworkFormat.ActivationFunction]
        ACTIVATION_SOFTMAX: _ClassVar[NetworkFormat.ActivationFunction]
    ACTIVATION_DEFAULT: NetworkFormat.ActivationFunction
    ACTIVATION_MISH: NetworkFormat.ActivationFunction
    ACTIVATION_RELU: NetworkFormat.ActivationFunction
    ACTIVATION_NONE: NetworkFormat.ActivationFunction
    ACTIVATION_TANH: NetworkFormat.ActivationFunction
    ACTIVATION_SIGMOID: NetworkFormat.ActivationFunction
    ACTIVATION_SELU: NetworkFormat.ActivationFunction
    ACTIVATION_SWISH: NetworkFormat.ActivationFunction
    ACTIVATION_RELU_2: NetworkFormat.ActivationFunction
    ACTIVATION_SOFTMAX: NetworkFormat.ActivationFunction
    class DefaultActivation(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        DEFAULT_ACTIVATION_RELU: _ClassVar[NetworkFormat.DefaultActivation]
        DEFAULT_ACTIVATION_MISH: _ClassVar[NetworkFormat.DefaultActivation]
    DEFAULT_ACTIVATION_RELU: NetworkFormat.DefaultActivation
    DEFAULT_ACTIVATION_MISH: NetworkFormat.DefaultActivation
    class InputEmbeddingFormat(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        INPUT_EMBEDDING_NONE: _ClassVar[NetworkFormat.InputEmbeddingFormat]
        INPUT_EMBEDDING_PE_MAP: _ClassVar[NetworkFormat.InputEmbeddingFormat]
        INPUT_EMBEDDING_PE_DENSE: _ClassVar[NetworkFormat.InputEmbeddingFormat]
    INPUT_EMBEDDING_NONE: NetworkFormat.InputEmbeddingFormat
    INPUT_EMBEDDING_PE_MAP: NetworkFormat.InputEmbeddingFormat
    INPUT_EMBEDDING_PE_DENSE: NetworkFormat.InputEmbeddingFormat
    INPUT_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_FIELD_NUMBER: _ClassVar[int]
    NETWORK_FIELD_NUMBER: _ClassVar[int]
    POLICY_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    MOVES_LEFT_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_ACTIVATION_FIELD_NUMBER: _ClassVar[int]
    SMOLGEN_ACTIVATION_FIELD_NUMBER: _ClassVar[int]
    FFN_ACTIVATION_FIELD_NUMBER: _ClassVar[int]
    INPUT_EMBEDDING_FIELD_NUMBER: _ClassVar[int]
    input: NetworkFormat.InputFormat
    output: NetworkFormat.OutputFormat
    network: NetworkFormat.NetworkStructure
    policy: NetworkFormat.PolicyFormat
    value: NetworkFormat.ValueFormat
    moves_left: NetworkFormat.MovesLeftFormat
    default_activation: NetworkFormat.DefaultActivation
    smolgen_activation: NetworkFormat.ActivationFunction
    ffn_activation: NetworkFormat.ActivationFunction
    input_embedding: NetworkFormat.InputEmbeddingFormat
    def __init__(self, input: _Optional[_Union[NetworkFormat.InputFormat, str]] = ..., output: _Optional[_Union[NetworkFormat.OutputFormat, str]] = ..., network: _Optional[_Union[NetworkFormat.NetworkStructure, str]] = ..., policy: _Optional[_Union[NetworkFormat.PolicyFormat, str]] = ..., value: _Optional[_Union[NetworkFormat.ValueFormat, str]] = ..., moves_left: _Optional[_Union[NetworkFormat.MovesLeftFormat, str]] = ..., default_activation: _Optional[_Union[NetworkFormat.DefaultActivation, str]] = ..., smolgen_activation: _Optional[_Union[NetworkFormat.ActivationFunction, str]] = ..., ffn_activation: _Optional[_Union[NetworkFormat.ActivationFunction, str]] = ..., input_embedding: _Optional[_Union[NetworkFormat.InputEmbeddingFormat, str]] = ...) -> None: ...

class Format(_message.Message):
    __slots__ = ("weights_encoding", "network_format")
    class Encoding(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        UNKNOWN: _ClassVar[Format.Encoding]
        LINEAR16: _ClassVar[Format.Encoding]
    UNKNOWN: Format.Encoding
    LINEAR16: Format.Encoding
    WEIGHTS_ENCODING_FIELD_NUMBER: _ClassVar[int]
    NETWORK_FORMAT_FIELD_NUMBER: _ClassVar[int]
    weights_encoding: Format.Encoding
    network_format: NetworkFormat
    def __init__(self, weights_encoding: _Optional[_Union[Format.Encoding, str]] = ..., network_format: _Optional[_Union[NetworkFormat, _Mapping]] = ...) -> None: ...

class OnnxModel(_message.Message):
    __slots__ = ("model", "data_type", "input_planes", "output_value", "output_wdl", "output_policy", "output_mlh")
    class DataType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        UNKNOWN_DATATYPE: _ClassVar[OnnxModel.DataType]
        FLOAT: _ClassVar[OnnxModel.DataType]
        FLOAT16: _ClassVar[OnnxModel.DataType]
        BFLOAT16: _ClassVar[OnnxModel.DataType]
    UNKNOWN_DATATYPE: OnnxModel.DataType
    FLOAT: OnnxModel.DataType
    FLOAT16: OnnxModel.DataType
    BFLOAT16: OnnxModel.DataType
    MODEL_FIELD_NUMBER: _ClassVar[int]
    DATA_TYPE_FIELD_NUMBER: _ClassVar[int]
    INPUT_PLANES_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_VALUE_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_WDL_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_POLICY_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_MLH_FIELD_NUMBER: _ClassVar[int]
    model: bytes
    data_type: OnnxModel.DataType
    input_planes: str
    output_value: str
    output_wdl: str
    output_policy: str
    output_mlh: str
    def __init__(self, model: _Optional[bytes] = ..., data_type: _Optional[_Union[OnnxModel.DataType, str]] = ..., input_planes: _Optional[str] = ..., output_value: _Optional[str] = ..., output_wdl: _Optional[str] = ..., output_policy: _Optional[str] = ..., output_mlh: _Optional[str] = ...) -> None: ...

class Net(_message.Message):
    __slots__ = ("magic", "license", "min_version", "format", "training_params", "weights", "onnx_model")
    MAGIC_FIELD_NUMBER: _ClassVar[int]
    LICENSE_FIELD_NUMBER: _ClassVar[int]
    MIN_VERSION_FIELD_NUMBER: _ClassVar[int]
    FORMAT_FIELD_NUMBER: _ClassVar[int]
    TRAINING_PARAMS_FIELD_NUMBER: _ClassVar[int]
    WEIGHTS_FIELD_NUMBER: _ClassVar[int]
    ONNX_MODEL_FIELD_NUMBER: _ClassVar[int]
    magic: int
    license: str
    min_version: EngineVersion
    format: Format
    training_params: TrainingParams
    weights: Weights
    onnx_model: OnnxModel
    def __init__(self, magic: _Optional[int] = ..., license: _Optional[str] = ..., min_version: _Optional[_Union[EngineVersion, _Mapping]] = ..., format: _Optional[_Union[Format, _Mapping]] = ..., training_params: _Optional[_Union[TrainingParams, _Mapping]] = ..., weights: _Optional[_Union[Weights, _Mapping]] = ..., onnx_model: _Optional[_Union[OnnxModel, _Mapping]] = ...) -> None: ...
