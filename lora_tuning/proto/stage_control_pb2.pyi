from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ShufflingChunkPoolControlRequest(_message.Message):
    __slots__ = ("reset_chunk_anchor", "set_chunk_anchor")
    RESET_CHUNK_ANCHOR_FIELD_NUMBER: _ClassVar[int]
    SET_CHUNK_ANCHOR_FIELD_NUMBER: _ClassVar[int]
    reset_chunk_anchor: bool
    set_chunk_anchor: str
    def __init__(self, reset_chunk_anchor: bool = ..., set_chunk_anchor: _Optional[str] = ...) -> None: ...

class StageControlRequest(_message.Message):
    __slots__ = ("chunk_pool_request",)
    CHUNK_POOL_REQUEST_FIELD_NUMBER: _ClassVar[int]
    chunk_pool_request: ShufflingChunkPoolControlRequest
    def __init__(self, chunk_pool_request: _Optional[_Union[ShufflingChunkPoolControlRequest, _Mapping]] = ...) -> None: ...

class ShufflingChunkPoolControlResponse(_message.Message):
    __slots__ = ("chunk_anchor", "chunks_since_anchor")
    CHUNK_ANCHOR_FIELD_NUMBER: _ClassVar[int]
    CHUNKS_SINCE_ANCHOR_FIELD_NUMBER: _ClassVar[int]
    chunk_anchor: str
    chunks_since_anchor: int
    def __init__(self, chunk_anchor: _Optional[str] = ..., chunks_since_anchor: _Optional[int] = ...) -> None: ...

class StageControlResponse(_message.Message):
    __slots__ = ("chunk_pool_response",)
    CHUNK_POOL_RESPONSE_FIELD_NUMBER: _ClassVar[int]
    chunk_pool_response: ShufflingChunkPoolControlResponse
    def __init__(self, chunk_pool_response: _Optional[_Union[ShufflingChunkPoolControlResponse, _Mapping]] = ...) -> None: ...
