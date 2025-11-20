from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class LoadMetricProto(_message.Message):
    __slots__ = ("name", "load_seconds", "total_seconds")
    NAME_FIELD_NUMBER: _ClassVar[int]
    LOAD_SECONDS_FIELD_NUMBER: _ClassVar[int]
    TOTAL_SECONDS_FIELD_NUMBER: _ClassVar[int]
    name: str
    load_seconds: float
    total_seconds: float
    def __init__(self, name: _Optional[str] = ..., load_seconds: _Optional[float] = ..., total_seconds: _Optional[float] = ...) -> None: ...

class StatisticsProtoInt64(_message.Message):
    __slots__ = ("min", "max", "sum", "count", "latest")
    MIN_FIELD_NUMBER: _ClassVar[int]
    MAX_FIELD_NUMBER: _ClassVar[int]
    SUM_FIELD_NUMBER: _ClassVar[int]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    LATEST_FIELD_NUMBER: _ClassVar[int]
    min: int
    max: int
    sum: int
    count: int
    latest: int
    def __init__(self, min: _Optional[int] = ..., max: _Optional[int] = ..., sum: _Optional[int] = ..., count: _Optional[int] = ..., latest: _Optional[int] = ...) -> None: ...

class StatisticsProtoDouble(_message.Message):
    __slots__ = ("name", "min", "max", "sum", "count", "latest")
    NAME_FIELD_NUMBER: _ClassVar[int]
    MIN_FIELD_NUMBER: _ClassVar[int]
    MAX_FIELD_NUMBER: _ClassVar[int]
    SUM_FIELD_NUMBER: _ClassVar[int]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    LATEST_FIELD_NUMBER: _ClassVar[int]
    name: str
    min: float
    max: float
    sum: float
    count: int
    latest: float
    def __init__(self, name: _Optional[str] = ..., min: _Optional[float] = ..., max: _Optional[float] = ..., sum: _Optional[float] = ..., count: _Optional[int] = ..., latest: _Optional[float] = ...) -> None: ...

class QueueMetricProto(_message.Message):
    __slots__ = ("name", "put_count", "get_count", "drop_count", "queue_fullness", "queue_capacity")
    NAME_FIELD_NUMBER: _ClassVar[int]
    PUT_COUNT_FIELD_NUMBER: _ClassVar[int]
    GET_COUNT_FIELD_NUMBER: _ClassVar[int]
    DROP_COUNT_FIELD_NUMBER: _ClassVar[int]
    QUEUE_FULLNESS_FIELD_NUMBER: _ClassVar[int]
    QUEUE_CAPACITY_FIELD_NUMBER: _ClassVar[int]
    name: str
    put_count: int
    get_count: int
    drop_count: int
    queue_fullness: StatisticsProtoInt64
    queue_capacity: int
    def __init__(self, name: _Optional[str] = ..., put_count: _Optional[int] = ..., get_count: _Optional[int] = ..., drop_count: _Optional[int] = ..., queue_fullness: _Optional[_Union[StatisticsProtoInt64, _Mapping]] = ..., queue_capacity: _Optional[int] = ...) -> None: ...

class CountMetricProto(_message.Message):
    __slots__ = ("name", "count")
    NAME_FIELD_NUMBER: _ClassVar[int]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    name: str
    count: int
    def __init__(self, name: _Optional[str] = ..., count: _Optional[int] = ...) -> None: ...

class GaugeMetricProto(_message.Message):
    __slots__ = ("name", "value", "capacity")
    NAME_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    CAPACITY_FIELD_NUMBER: _ClassVar[int]
    name: str
    value: int
    capacity: int
    def __init__(self, name: _Optional[str] = ..., value: _Optional[int] = ..., capacity: _Optional[int] = ...) -> None: ...

class StageMetricProto(_message.Message):
    __slots__ = ("name", "load_metrics", "queue_metrics", "count_metrics", "gauge_metrics", "statistics_metrics", "last_chunk_key", "anchor")
    NAME_FIELD_NUMBER: _ClassVar[int]
    LOAD_METRICS_FIELD_NUMBER: _ClassVar[int]
    QUEUE_METRICS_FIELD_NUMBER: _ClassVar[int]
    COUNT_METRICS_FIELD_NUMBER: _ClassVar[int]
    GAUGE_METRICS_FIELD_NUMBER: _ClassVar[int]
    STATISTICS_METRICS_FIELD_NUMBER: _ClassVar[int]
    LAST_CHUNK_KEY_FIELD_NUMBER: _ClassVar[int]
    ANCHOR_FIELD_NUMBER: _ClassVar[int]
    name: str
    load_metrics: _containers.RepeatedCompositeFieldContainer[LoadMetricProto]
    queue_metrics: _containers.RepeatedCompositeFieldContainer[QueueMetricProto]
    count_metrics: _containers.RepeatedCompositeFieldContainer[CountMetricProto]
    gauge_metrics: _containers.RepeatedCompositeFieldContainer[GaugeMetricProto]
    statistics_metrics: _containers.RepeatedCompositeFieldContainer[StatisticsProtoDouble]
    last_chunk_key: str
    anchor: str
    def __init__(self, name: _Optional[str] = ..., load_metrics: _Optional[_Iterable[_Union[LoadMetricProto, _Mapping]]] = ..., queue_metrics: _Optional[_Iterable[_Union[QueueMetricProto, _Mapping]]] = ..., count_metrics: _Optional[_Iterable[_Union[CountMetricProto, _Mapping]]] = ..., gauge_metrics: _Optional[_Iterable[_Union[GaugeMetricProto, _Mapping]]] = ..., statistics_metrics: _Optional[_Iterable[_Union[StatisticsProtoDouble, _Mapping]]] = ..., last_chunk_key: _Optional[str] = ..., anchor: _Optional[str] = ...) -> None: ...

class DataLoaderMetricsProto(_message.Message):
    __slots__ = ("stage_metrics",)
    STAGE_METRICS_FIELD_NUMBER: _ClassVar[int]
    stage_metrics: _containers.RepeatedCompositeFieldContainer[StageMetricProto]
    def __init__(self, stage_metrics: _Optional[_Iterable[_Union[StageMetricProto, _Mapping]]] = ...) -> None: ...
