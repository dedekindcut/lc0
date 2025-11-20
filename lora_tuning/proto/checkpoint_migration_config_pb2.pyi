from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CheckpointMigrationRule(_message.Message):
    __slots__ = ("from_path", "to_path")
    FROM_PATH_FIELD_NUMBER: _ClassVar[int]
    TO_PATH_FIELD_NUMBER: _ClassVar[int]
    from_path: str
    to_path: str
    def __init__(self, from_path: _Optional[str] = ..., to_path: _Optional[str] = ...) -> None: ...

class CheckpointMigrationConfig(_message.Message):
    __slots__ = ("rule",)
    RULE_FIELD_NUMBER: _ClassVar[int]
    rule: _containers.RepeatedCompositeFieldContainer[CheckpointMigrationRule]
    def __init__(self, rule: _Optional[_Iterable[_Union[CheckpointMigrationRule, _Mapping]]] = ...) -> None: ...
