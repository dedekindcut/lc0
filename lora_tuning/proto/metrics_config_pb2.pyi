from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class TrainingBatch(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class MetricConfig(_message.Message):
    __slots__ = ("name", "use_swa_model", "period", "use_global_steps", "after_epoch", "training_batch", "dataloader_output", "npz_filename")
    NAME_FIELD_NUMBER: _ClassVar[int]
    USE_SWA_MODEL_FIELD_NUMBER: _ClassVar[int]
    PERIOD_FIELD_NUMBER: _ClassVar[int]
    USE_GLOBAL_STEPS_FIELD_NUMBER: _ClassVar[int]
    AFTER_EPOCH_FIELD_NUMBER: _ClassVar[int]
    TRAINING_BATCH_FIELD_NUMBER: _ClassVar[int]
    DATALOADER_OUTPUT_FIELD_NUMBER: _ClassVar[int]
    NPZ_FILENAME_FIELD_NUMBER: _ClassVar[int]
    name: str
    use_swa_model: bool
    period: int
    use_global_steps: bool
    after_epoch: bool
    training_batch: TrainingBatch
    dataloader_output: str
    npz_filename: str
    def __init__(self, name: _Optional[str] = ..., use_swa_model: bool = ..., period: _Optional[int] = ..., use_global_steps: bool = ..., after_epoch: bool = ..., training_batch: _Optional[_Union[TrainingBatch, _Mapping]] = ..., dataloader_output: _Optional[str] = ..., npz_filename: _Optional[str] = ...) -> None: ...

class MetricsConfig(_message.Message):
    __slots__ = ("tensorboard_path", "metric")
    TENSORBOARD_PATH_FIELD_NUMBER: _ClassVar[int]
    METRIC_FIELD_NUMBER: _ClassVar[int]
    tensorboard_path: str
    metric: _containers.RepeatedCompositeFieldContainer[MetricConfig]
    def __init__(self, tensorboard_path: _Optional[str] = ..., metric: _Optional[_Iterable[_Union[MetricConfig, _Mapping]]] = ...) -> None: ...
