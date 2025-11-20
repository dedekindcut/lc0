from proto import data_loader_config_pb2 as _data_loader_config_pb2
from proto import model_config_pb2 as _model_config_pb2
from proto import training_config_pb2 as _training_config_pb2
from proto import metrics_config_pb2 as _metrics_config_pb2
from proto import export_config_pb2 as _export_config_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class RootConfig(_message.Message):
    __slots__ = ("name", "log_filename", "data_loader", "training", "model", "metrics", "export")
    NAME_FIELD_NUMBER: _ClassVar[int]
    LOG_FILENAME_FIELD_NUMBER: _ClassVar[int]
    DATA_LOADER_FIELD_NUMBER: _ClassVar[int]
    TRAINING_FIELD_NUMBER: _ClassVar[int]
    MODEL_FIELD_NUMBER: _ClassVar[int]
    METRICS_FIELD_NUMBER: _ClassVar[int]
    EXPORT_FIELD_NUMBER: _ClassVar[int]
    name: str
    log_filename: str
    data_loader: _data_loader_config_pb2.DataLoaderConfig
    training: _training_config_pb2.TrainingConfig
    model: _model_config_pb2.ModelConfig
    metrics: _metrics_config_pb2.MetricsConfig
    export: _export_config_pb2.ExportConfig
    def __init__(self, name: _Optional[str] = ..., log_filename: _Optional[str] = ..., data_loader: _Optional[_Union[_data_loader_config_pb2.DataLoaderConfig, _Mapping]] = ..., training: _Optional[_Union[_training_config_pb2.TrainingConfig, _Mapping]] = ..., model: _Optional[_Union[_model_config_pb2.ModelConfig, _Mapping]] = ..., metrics: _Optional[_Union[_metrics_config_pb2.MetricsConfig, _Mapping]] = ..., export: _Optional[_Union[_export_config_pb2.ExportConfig, _Mapping]] = ...) -> None: ...
