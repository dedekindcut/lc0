from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class TrainingConfig(_message.Message):
    __slots__ = ("schedule", "lr_schedule", "checkpoint", "optimizer", "losses", "max_grad_norm", "swa")
    SCHEDULE_FIELD_NUMBER: _ClassVar[int]
    LR_SCHEDULE_FIELD_NUMBER: _ClassVar[int]
    CHECKPOINT_FIELD_NUMBER: _ClassVar[int]
    OPTIMIZER_FIELD_NUMBER: _ClassVar[int]
    LOSSES_FIELD_NUMBER: _ClassVar[int]
    MAX_GRAD_NORM_FIELD_NUMBER: _ClassVar[int]
    SWA_FIELD_NUMBER: _ClassVar[int]
    schedule: ScheduleConfig
    lr_schedule: _containers.RepeatedCompositeFieldContainer[LrSchedule]
    checkpoint: CheckpointConfig
    optimizer: OptimizerConfig
    losses: LossWeightsConfig
    max_grad_norm: float
    swa: SWAConfig
    def __init__(self, schedule: _Optional[_Union[ScheduleConfig, _Mapping]] = ..., lr_schedule: _Optional[_Iterable[_Union[LrSchedule, _Mapping]]] = ..., checkpoint: _Optional[_Union[CheckpointConfig, _Mapping]] = ..., optimizer: _Optional[_Union[OptimizerConfig, _Mapping]] = ..., losses: _Optional[_Union[LossWeightsConfig, _Mapping]] = ..., max_grad_norm: _Optional[float] = ..., swa: _Optional[_Union[SWAConfig, _Mapping]] = ...) -> None: ...

class ScheduleConfig(_message.Message):
    __slots__ = ("steps_per_network", "chunks_per_network")
    STEPS_PER_NETWORK_FIELD_NUMBER: _ClassVar[int]
    CHUNKS_PER_NETWORK_FIELD_NUMBER: _ClassVar[int]
    steps_per_network: int
    chunks_per_network: int
    def __init__(self, steps_per_network: _Optional[int] = ..., chunks_per_network: _Optional[int] = ...) -> None: ...

class OptimizerConfig(_message.Message):
    __slots__ = ("nadamw", "momentum")
    NADAMW_FIELD_NUMBER: _ClassVar[int]
    MOMENTUM_FIELD_NUMBER: _ClassVar[int]
    nadamw: NadamwOptimizerConfig
    momentum: float
    def __init__(self, nadamw: _Optional[_Union[NadamwOptimizerConfig, _Mapping]] = ..., momentum: _Optional[float] = ...) -> None: ...

class LrSchedule(_message.Message):
    __slots__ = ("starting_step", "duration_steps", "lr", "transition", "loop")
    class Transition(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        CONSTANT: _ClassVar[LrSchedule.Transition]
        LINEAR: _ClassVar[LrSchedule.Transition]
        COSINE: _ClassVar[LrSchedule.Transition]
    CONSTANT: LrSchedule.Transition
    LINEAR: LrSchedule.Transition
    COSINE: LrSchedule.Transition
    STARTING_STEP_FIELD_NUMBER: _ClassVar[int]
    DURATION_STEPS_FIELD_NUMBER: _ClassVar[int]
    LR_FIELD_NUMBER: _ClassVar[int]
    TRANSITION_FIELD_NUMBER: _ClassVar[int]
    LOOP_FIELD_NUMBER: _ClassVar[int]
    starting_step: int
    duration_steps: _containers.RepeatedScalarFieldContainer[int]
    lr: _containers.RepeatedScalarFieldContainer[float]
    transition: _containers.RepeatedScalarFieldContainer[LrSchedule.Transition]
    loop: bool
    def __init__(self, starting_step: _Optional[int] = ..., duration_steps: _Optional[_Iterable[int]] = ..., lr: _Optional[_Iterable[float]] = ..., transition: _Optional[_Iterable[_Union[LrSchedule.Transition, str]]] = ..., loop: bool = ...) -> None: ...

class NadamwOptimizerConfig(_message.Message):
    __slots__ = ("beta_1", "beta_2", "epsilon", "weight_decay", "decay_embedding", "decay_biases", "decay_layer_norms")
    BETA_1_FIELD_NUMBER: _ClassVar[int]
    BETA_2_FIELD_NUMBER: _ClassVar[int]
    EPSILON_FIELD_NUMBER: _ClassVar[int]
    WEIGHT_DECAY_FIELD_NUMBER: _ClassVar[int]
    DECAY_EMBEDDING_FIELD_NUMBER: _ClassVar[int]
    DECAY_BIASES_FIELD_NUMBER: _ClassVar[int]
    DECAY_LAYER_NORMS_FIELD_NUMBER: _ClassVar[int]
    beta_1: float
    beta_2: float
    epsilon: float
    weight_decay: float
    decay_embedding: bool
    decay_biases: bool
    decay_layer_norms: bool
    def __init__(self, beta_1: _Optional[float] = ..., beta_2: _Optional[float] = ..., epsilon: _Optional[float] = ..., weight_decay: _Optional[float] = ..., decay_embedding: bool = ..., decay_biases: bool = ..., decay_layer_norms: bool = ...) -> None: ...

class CheckpointConfig(_message.Message):
    __slots__ = ("path", "max_to_keep")
    PATH_FIELD_NUMBER: _ClassVar[int]
    MAX_TO_KEEP_FIELD_NUMBER: _ClassVar[int]
    path: str
    max_to_keep: int
    def __init__(self, path: _Optional[str] = ..., max_to_keep: _Optional[int] = ...) -> None: ...

class LossWeightsConfig(_message.Message):
    __slots__ = ("policy", "value", "movesleft")
    POLICY_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    MOVESLEFT_FIELD_NUMBER: _ClassVar[int]
    policy: _containers.RepeatedCompositeFieldContainer[PolicyLossWeightsConfig]
    value: _containers.RepeatedCompositeFieldContainer[ValueLossWeightsConfig]
    movesleft: _containers.RepeatedCompositeFieldContainer[MovesLeftLossWeightsConfig]
    def __init__(self, policy: _Optional[_Iterable[_Union[PolicyLossWeightsConfig, _Mapping]]] = ..., value: _Optional[_Iterable[_Union[ValueLossWeightsConfig, _Mapping]]] = ..., movesleft: _Optional[_Iterable[_Union[MovesLeftLossWeightsConfig, _Mapping]]] = ...) -> None: ...

class PolicyLossWeightsConfig(_message.Message):
    __slots__ = ("name", "weight", "illegal_moves", "type", "temperature")
    class IllegalMoveHandling(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        TRAIN_TO_ZERO: _ClassVar[PolicyLossWeightsConfig.IllegalMoveHandling]
        MASK: _ClassVar[PolicyLossWeightsConfig.IllegalMoveHandling]
    TRAIN_TO_ZERO: PolicyLossWeightsConfig.IllegalMoveHandling
    MASK: PolicyLossWeightsConfig.IllegalMoveHandling
    class LossType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        LOSS_TYPE_UNSPECIFIED: _ClassVar[PolicyLossWeightsConfig.LossType]
        CROSS_ENTROPY: _ClassVar[PolicyLossWeightsConfig.LossType]
        KL: _ClassVar[PolicyLossWeightsConfig.LossType]
    LOSS_TYPE_UNSPECIFIED: PolicyLossWeightsConfig.LossType
    CROSS_ENTROPY: PolicyLossWeightsConfig.LossType
    KL: PolicyLossWeightsConfig.LossType
    NAME_FIELD_NUMBER: _ClassVar[int]
    WEIGHT_FIELD_NUMBER: _ClassVar[int]
    ILLEGAL_MOVES_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    TEMPERATURE_FIELD_NUMBER: _ClassVar[int]
    name: str
    weight: float
    illegal_moves: PolicyLossWeightsConfig.IllegalMoveHandling
    type: PolicyLossWeightsConfig.LossType
    temperature: float
    def __init__(self, name: _Optional[str] = ..., weight: _Optional[float] = ..., illegal_moves: _Optional[_Union[PolicyLossWeightsConfig.IllegalMoveHandling, str]] = ..., type: _Optional[_Union[PolicyLossWeightsConfig.LossType, str]] = ..., temperature: _Optional[float] = ...) -> None: ...

class ValueLossWeightsConfig(_message.Message):
    __slots__ = ("name", "weight")
    NAME_FIELD_NUMBER: _ClassVar[int]
    WEIGHT_FIELD_NUMBER: _ClassVar[int]
    name: str
    weight: float
    def __init__(self, name: _Optional[str] = ..., weight: _Optional[float] = ...) -> None: ...

class MovesLeftLossWeightsConfig(_message.Message):
    __slots__ = ("name", "weight")
    NAME_FIELD_NUMBER: _ClassVar[int]
    WEIGHT_FIELD_NUMBER: _ClassVar[int]
    name: str
    weight: float
    def __init__(self, name: _Optional[str] = ..., weight: _Optional[float] = ...) -> None: ...

class SWAConfig(_message.Message):
    __slots__ = ("period_steps", "num_averages")
    PERIOD_STEPS_FIELD_NUMBER: _ClassVar[int]
    NUM_AVERAGES_FIELD_NUMBER: _ClassVar[int]
    period_steps: int
    num_averages: int
    def __init__(self, period_steps: _Optional[int] = ..., num_averages: _Optional[int] = ...) -> None: ...
