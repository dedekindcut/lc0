from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class ExportConfig(_message.Message):
    __slots__ = ("path", "upload_training_run", "export_swa_model")
    PATH_FIELD_NUMBER: _ClassVar[int]
    UPLOAD_TRAINING_RUN_FIELD_NUMBER: _ClassVar[int]
    EXPORT_SWA_MODEL_FIELD_NUMBER: _ClassVar[int]
    path: str
    upload_training_run: int
    export_swa_model: bool
    def __init__(self, path: _Optional[str] = ..., upload_training_run: _Optional[int] = ..., export_swa_model: bool = ...) -> None: ...
