from proto import net_pb2 as _net_pb2
from proto import hlo_pb2 as _hlo_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ModelConfig(_message.Message):
    __slots__ = ("defaults", "embedding", "encoder", "policy_head", "value_head", "movesleft_head")
    DEFAULTS_FIELD_NUMBER: _ClassVar[int]
    EMBEDDING_FIELD_NUMBER: _ClassVar[int]
    ENCODER_FIELD_NUMBER: _ClassVar[int]
    POLICY_HEAD_FIELD_NUMBER: _ClassVar[int]
    VALUE_HEAD_FIELD_NUMBER: _ClassVar[int]
    MOVESLEFT_HEAD_FIELD_NUMBER: _ClassVar[int]
    defaults: DefaultsConfig
    embedding: EmbeddingConfig
    encoder: EncoderConfig
    policy_head: PolicyHeadConfig
    value_head: ValueHeadConfig
    movesleft_head: MovesLeftHeadConfig
    def __init__(self, defaults: _Optional[_Union[DefaultsConfig, _Mapping]] = ..., embedding: _Optional[_Union[EmbeddingConfig, _Mapping]] = ..., encoder: _Optional[_Union[EncoderConfig, _Mapping]] = ..., policy_head: _Optional[_Union[PolicyHeadConfig, _Mapping]] = ..., value_head: _Optional[_Union[ValueHeadConfig, _Mapping]] = ..., movesleft_head: _Optional[_Union[MovesLeftHeadConfig, _Mapping]] = ...) -> None: ...

class DefaultsConfig(_message.Message):
    __slots__ = ("compute_dtype", "activation", "ffn_activation")
    COMPUTE_DTYPE_FIELD_NUMBER: _ClassVar[int]
    ACTIVATION_FIELD_NUMBER: _ClassVar[int]
    FFN_ACTIVATION_FIELD_NUMBER: _ClassVar[int]
    compute_dtype: _hlo_pb2.XlaShapeProto.Type
    activation: _net_pb2.NetworkFormat.ActivationFunction
    ffn_activation: _net_pb2.NetworkFormat.ActivationFunction
    def __init__(self, compute_dtype: _Optional[_Union[_hlo_pb2.XlaShapeProto.Type, str]] = ..., activation: _Optional[_Union[_net_pb2.NetworkFormat.ActivationFunction, str]] = ..., ffn_activation: _Optional[_Union[_net_pb2.NetworkFormat.ActivationFunction, str]] = ...) -> None: ...

class EmbeddingConfig(_message.Message):
    __slots__ = ("dense_size", "embedding_size", "dff")
    DENSE_SIZE_FIELD_NUMBER: _ClassVar[int]
    EMBEDDING_SIZE_FIELD_NUMBER: _ClassVar[int]
    DFF_FIELD_NUMBER: _ClassVar[int]
    dense_size: int
    embedding_size: int
    dff: int
    def __init__(self, dense_size: _Optional[int] = ..., embedding_size: _Optional[int] = ..., dff: _Optional[int] = ...) -> None: ...

class EncoderConfig(_message.Message):
    __slots__ = ("num_blocks", "dff", "d_model", "heads", "smolgen")
    NUM_BLOCKS_FIELD_NUMBER: _ClassVar[int]
    DFF_FIELD_NUMBER: _ClassVar[int]
    D_MODEL_FIELD_NUMBER: _ClassVar[int]
    HEADS_FIELD_NUMBER: _ClassVar[int]
    SMOLGEN_FIELD_NUMBER: _ClassVar[int]
    num_blocks: int
    dff: int
    d_model: int
    heads: int
    smolgen: SmolgenConfig
    def __init__(self, num_blocks: _Optional[int] = ..., dff: _Optional[int] = ..., d_model: _Optional[int] = ..., heads: _Optional[int] = ..., smolgen: _Optional[_Union[SmolgenConfig, _Mapping]] = ...) -> None: ...

class SmolgenConfig(_message.Message):
    __slots__ = ("hidden_channels", "hidden_size", "gen_size", "activation")
    HIDDEN_CHANNELS_FIELD_NUMBER: _ClassVar[int]
    HIDDEN_SIZE_FIELD_NUMBER: _ClassVar[int]
    GEN_SIZE_FIELD_NUMBER: _ClassVar[int]
    ACTIVATION_FIELD_NUMBER: _ClassVar[int]
    hidden_channels: int
    hidden_size: int
    gen_size: int
    activation: _net_pb2.NetworkFormat.ActivationFunction
    def __init__(self, hidden_channels: _Optional[int] = ..., hidden_size: _Optional[int] = ..., gen_size: _Optional[int] = ..., activation: _Optional[_Union[_net_pb2.NetworkFormat.ActivationFunction, str]] = ...) -> None: ...

class PolicyHeadConfig(_message.Message):
    __slots__ = ("embedding_size", "d_model")
    EMBEDDING_SIZE_FIELD_NUMBER: _ClassVar[int]
    D_MODEL_FIELD_NUMBER: _ClassVar[int]
    embedding_size: int
    d_model: int
    def __init__(self, embedding_size: _Optional[int] = ..., d_model: _Optional[int] = ...) -> None: ...

class ValueHeadConfig(_message.Message):
    __slots__ = ("num_channels",)
    NUM_CHANNELS_FIELD_NUMBER: _ClassVar[int]
    num_channels: int
    def __init__(self, num_channels: _Optional[int] = ...) -> None: ...

class MovesLeftHeadConfig(_message.Message):
    __slots__ = ("num_channels",)
    NUM_CHANNELS_FIELD_NUMBER: _ClassVar[int]
    num_channels: int
    def __init__(self, num_channels: _Optional[int] = ...) -> None: ...
