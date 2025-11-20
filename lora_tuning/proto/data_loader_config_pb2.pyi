from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class QueueConfig(_message.Message):
    __slots__ = ("name", "queue_capacity", "overflow_behavior")
    class OverflowBehavior(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        BLOCK: _ClassVar[QueueConfig.OverflowBehavior]
        DROP_NEW: _ClassVar[QueueConfig.OverflowBehavior]
        KEEP_NEWEST: _ClassVar[QueueConfig.OverflowBehavior]
    BLOCK: QueueConfig.OverflowBehavior
    DROP_NEW: QueueConfig.OverflowBehavior
    KEEP_NEWEST: QueueConfig.OverflowBehavior
    NAME_FIELD_NUMBER: _ClassVar[int]
    QUEUE_CAPACITY_FIELD_NUMBER: _ClassVar[int]
    OVERFLOW_BEHAVIOR_FIELD_NUMBER: _ClassVar[int]
    name: str
    queue_capacity: int
    overflow_behavior: QueueConfig.OverflowBehavior
    def __init__(self, name: _Optional[str] = ..., queue_capacity: _Optional[int] = ..., overflow_behavior: _Optional[_Union[QueueConfig.OverflowBehavior, str]] = ...) -> None: ...

class FilePathProviderConfig(_message.Message):
    __slots__ = ("directory", "output")
    DIRECTORY_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_FIELD_NUMBER: _ClassVar[int]
    directory: str
    output: QueueConfig
    def __init__(self, directory: _Optional[str] = ..., output: _Optional[_Union[QueueConfig, _Mapping]] = ...) -> None: ...

class ChunkSourceLoaderConfig(_message.Message):
    __slots__ = ("threads", "output")
    THREADS_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_FIELD_NUMBER: _ClassVar[int]
    threads: int
    output: QueueConfig
    def __init__(self, threads: _Optional[int] = ..., output: _Optional[_Union[QueueConfig, _Mapping]] = ...) -> None: ...

class PositionSamplingConfig(_message.Message):
    __slots__ = ("diff_focus_q_weight", "diff_focus_pol_scale", "diff_focus_alpha", "diff_focus_beta", "diff_focus_gamma", "diff_focus_tau", "default_weight")
    DIFF_FOCUS_Q_WEIGHT_FIELD_NUMBER: _ClassVar[int]
    DIFF_FOCUS_POL_SCALE_FIELD_NUMBER: _ClassVar[int]
    DIFF_FOCUS_ALPHA_FIELD_NUMBER: _ClassVar[int]
    DIFF_FOCUS_BETA_FIELD_NUMBER: _ClassVar[int]
    DIFF_FOCUS_GAMMA_FIELD_NUMBER: _ClassVar[int]
    DIFF_FOCUS_TAU_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_WEIGHT_FIELD_NUMBER: _ClassVar[int]
    diff_focus_q_weight: float
    diff_focus_pol_scale: float
    diff_focus_alpha: float
    diff_focus_beta: float
    diff_focus_gamma: float
    diff_focus_tau: float
    default_weight: float
    def __init__(self, diff_focus_q_weight: _Optional[float] = ..., diff_focus_pol_scale: _Optional[float] = ..., diff_focus_alpha: _Optional[float] = ..., diff_focus_beta: _Optional[float] = ..., diff_focus_gamma: _Optional[float] = ..., diff_focus_tau: _Optional[float] = ..., default_weight: _Optional[float] = ...) -> None: ...

class ShufflingChunkPoolConfig(_message.Message):
    __slots__ = ("chunk_pool_size", "source_ingestion_threads", "chunk_loading_threads", "output", "hanse_sampling_threshold", "hanse_sampling_gamma", "position_sampling", "cachehit_output", "position_cache_size", "caching_threads")
    CHUNK_POOL_SIZE_FIELD_NUMBER: _ClassVar[int]
    SOURCE_INGESTION_THREADS_FIELD_NUMBER: _ClassVar[int]
    CHUNK_LOADING_THREADS_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_FIELD_NUMBER: _ClassVar[int]
    HANSE_SAMPLING_THRESHOLD_FIELD_NUMBER: _ClassVar[int]
    HANSE_SAMPLING_GAMMA_FIELD_NUMBER: _ClassVar[int]
    POSITION_SAMPLING_FIELD_NUMBER: _ClassVar[int]
    CACHEHIT_OUTPUT_FIELD_NUMBER: _ClassVar[int]
    POSITION_CACHE_SIZE_FIELD_NUMBER: _ClassVar[int]
    CACHING_THREADS_FIELD_NUMBER: _ClassVar[int]
    chunk_pool_size: int
    source_ingestion_threads: int
    chunk_loading_threads: int
    output: QueueConfig
    hanse_sampling_threshold: int
    hanse_sampling_gamma: float
    position_sampling: PositionSamplingConfig
    cachehit_output: QueueConfig
    position_cache_size: int
    caching_threads: int
    def __init__(self, chunk_pool_size: _Optional[int] = ..., source_ingestion_threads: _Optional[int] = ..., chunk_loading_threads: _Optional[int] = ..., output: _Optional[_Union[QueueConfig, _Mapping]] = ..., hanse_sampling_threshold: _Optional[int] = ..., hanse_sampling_gamma: _Optional[float] = ..., position_sampling: _Optional[_Union[PositionSamplingConfig, _Mapping]] = ..., cachehit_output: _Optional[_Union[QueueConfig, _Mapping]] = ..., position_cache_size: _Optional[int] = ..., caching_threads: _Optional[int] = ...) -> None: ...

class ChunkRescorerConfig(_message.Message):
    __slots__ = ("threads", "output", "syzygy_paths", "dist_temp", "dist_offset", "dtz_boost", "new_input_format", "deblunder_threshold", "deblunder_width", "gaviota_paths")
    THREADS_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_FIELD_NUMBER: _ClassVar[int]
    SYZYGY_PATHS_FIELD_NUMBER: _ClassVar[int]
    DIST_TEMP_FIELD_NUMBER: _ClassVar[int]
    DIST_OFFSET_FIELD_NUMBER: _ClassVar[int]
    DTZ_BOOST_FIELD_NUMBER: _ClassVar[int]
    NEW_INPUT_FORMAT_FIELD_NUMBER: _ClassVar[int]
    DEBLUNDER_THRESHOLD_FIELD_NUMBER: _ClassVar[int]
    DEBLUNDER_WIDTH_FIELD_NUMBER: _ClassVar[int]
    GAVIOTA_PATHS_FIELD_NUMBER: _ClassVar[int]
    threads: int
    output: QueueConfig
    syzygy_paths: str
    dist_temp: float
    dist_offset: float
    dtz_boost: float
    new_input_format: int
    deblunder_threshold: float
    deblunder_width: float
    gaviota_paths: str
    def __init__(self, threads: _Optional[int] = ..., output: _Optional[_Union[QueueConfig, _Mapping]] = ..., syzygy_paths: _Optional[str] = ..., dist_temp: _Optional[float] = ..., dist_offset: _Optional[float] = ..., dtz_boost: _Optional[float] = ..., new_input_format: _Optional[int] = ..., deblunder_threshold: _Optional[float] = ..., deblunder_width: _Optional[float] = ..., gaviota_paths: _Optional[str] = ...) -> None: ...

class ChunkUnpackerConfig(_message.Message):
    __slots__ = ("threads", "position_sampling_rate", "position_count", "output", "prefetch_count", "prefetch_output", "position_sampling")
    THREADS_FIELD_NUMBER: _ClassVar[int]
    POSITION_SAMPLING_RATE_FIELD_NUMBER: _ClassVar[int]
    POSITION_COUNT_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_FIELD_NUMBER: _ClassVar[int]
    PREFETCH_COUNT_FIELD_NUMBER: _ClassVar[int]
    PREFETCH_OUTPUT_FIELD_NUMBER: _ClassVar[int]
    POSITION_SAMPLING_FIELD_NUMBER: _ClassVar[int]
    threads: int
    position_sampling_rate: float
    position_count: int
    output: QueueConfig
    prefetch_count: int
    prefetch_output: QueueConfig
    position_sampling: PositionSamplingConfig
    def __init__(self, threads: _Optional[int] = ..., position_sampling_rate: _Optional[float] = ..., position_count: _Optional[int] = ..., output: _Optional[_Union[QueueConfig, _Mapping]] = ..., prefetch_count: _Optional[int] = ..., prefetch_output: _Optional[_Union[QueueConfig, _Mapping]] = ..., position_sampling: _Optional[_Union[PositionSamplingConfig, _Mapping]] = ...) -> None: ...

class ShufflingFrameSamplerConfig(_message.Message):
    __slots__ = ("threads", "reservoir_size_per_thread", "output")
    THREADS_FIELD_NUMBER: _ClassVar[int]
    RESERVOIR_SIZE_PER_THREAD_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_FIELD_NUMBER: _ClassVar[int]
    threads: int
    reservoir_size_per_thread: int
    output: QueueConfig
    def __init__(self, threads: _Optional[int] = ..., reservoir_size_per_thread: _Optional[int] = ..., output: _Optional[_Union[QueueConfig, _Mapping]] = ...) -> None: ...

class TensorGeneratorConfig(_message.Message):
    __slots__ = ("threads", "batch_size", "output")
    THREADS_FIELD_NUMBER: _ClassVar[int]
    BATCH_SIZE_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_FIELD_NUMBER: _ClassVar[int]
    threads: int
    batch_size: int
    output: QueueConfig
    def __init__(self, threads: _Optional[int] = ..., batch_size: _Optional[int] = ..., output: _Optional[_Union[QueueConfig, _Mapping]] = ...) -> None: ...

class ChunkSourceSplitterConfig(_message.Message):
    __slots__ = ("output", "weight")
    OUTPUT_FIELD_NUMBER: _ClassVar[int]
    WEIGHT_FIELD_NUMBER: _ClassVar[int]
    output: _containers.RepeatedCompositeFieldContainer[QueueConfig]
    weight: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, output: _Optional[_Iterable[_Union[QueueConfig, _Mapping]]] = ..., weight: _Optional[_Iterable[int]] = ...) -> None: ...

class SimpleChunkExtractorConfig(_message.Message):
    __slots__ = ("output",)
    OUTPUT_FIELD_NUMBER: _ClassVar[int]
    output: QueueConfig
    def __init__(self, output: _Optional[_Union[QueueConfig, _Mapping]] = ...) -> None: ...

class JoinPositionsConfig(_message.Message):
    __slots__ = ("output",)
    OUTPUT_FIELD_NUMBER: _ClassVar[int]
    output: QueueConfig
    def __init__(self, output: _Optional[_Union[QueueConfig, _Mapping]] = ...) -> None: ...

class StageConfig(_message.Message):
    __slots__ = ("name", "input", "file_path_provider", "chunk_source_loader", "shuffling_chunk_pool", "chunk_unpacker", "shuffling_frame_sampler", "tensor_generator", "chunk_rescorer", "chunk_source_splitter", "simple_chunk_extractor", "join_positions")
    NAME_FIELD_NUMBER: _ClassVar[int]
    INPUT_FIELD_NUMBER: _ClassVar[int]
    FILE_PATH_PROVIDER_FIELD_NUMBER: _ClassVar[int]
    CHUNK_SOURCE_LOADER_FIELD_NUMBER: _ClassVar[int]
    SHUFFLING_CHUNK_POOL_FIELD_NUMBER: _ClassVar[int]
    CHUNK_UNPACKER_FIELD_NUMBER: _ClassVar[int]
    SHUFFLING_FRAME_SAMPLER_FIELD_NUMBER: _ClassVar[int]
    TENSOR_GENERATOR_FIELD_NUMBER: _ClassVar[int]
    CHUNK_RESCORER_FIELD_NUMBER: _ClassVar[int]
    CHUNK_SOURCE_SPLITTER_FIELD_NUMBER: _ClassVar[int]
    SIMPLE_CHUNK_EXTRACTOR_FIELD_NUMBER: _ClassVar[int]
    JOIN_POSITIONS_FIELD_NUMBER: _ClassVar[int]
    name: str
    input: _containers.RepeatedScalarFieldContainer[str]
    file_path_provider: FilePathProviderConfig
    chunk_source_loader: ChunkSourceLoaderConfig
    shuffling_chunk_pool: ShufflingChunkPoolConfig
    chunk_unpacker: ChunkUnpackerConfig
    shuffling_frame_sampler: ShufflingFrameSamplerConfig
    tensor_generator: TensorGeneratorConfig
    chunk_rescorer: ChunkRescorerConfig
    chunk_source_splitter: ChunkSourceSplitterConfig
    simple_chunk_extractor: SimpleChunkExtractorConfig
    join_positions: JoinPositionsConfig
    def __init__(self, name: _Optional[str] = ..., input: _Optional[_Iterable[str]] = ..., file_path_provider: _Optional[_Union[FilePathProviderConfig, _Mapping]] = ..., chunk_source_loader: _Optional[_Union[ChunkSourceLoaderConfig, _Mapping]] = ..., shuffling_chunk_pool: _Optional[_Union[ShufflingChunkPoolConfig, _Mapping]] = ..., chunk_unpacker: _Optional[_Union[ChunkUnpackerConfig, _Mapping]] = ..., shuffling_frame_sampler: _Optional[_Union[ShufflingFrameSamplerConfig, _Mapping]] = ..., tensor_generator: _Optional[_Union[TensorGeneratorConfig, _Mapping]] = ..., chunk_rescorer: _Optional[_Union[ChunkRescorerConfig, _Mapping]] = ..., chunk_source_splitter: _Optional[_Union[ChunkSourceSplitterConfig, _Mapping]] = ..., simple_chunk_extractor: _Optional[_Union[SimpleChunkExtractorConfig, _Mapping]] = ..., join_positions: _Optional[_Union[JoinPositionsConfig, _Mapping]] = ...) -> None: ...

class DataLoaderConfig(_message.Message):
    __slots__ = ("stage", "output")
    STAGE_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_FIELD_NUMBER: _ClassVar[int]
    stage: _containers.RepeatedCompositeFieldContainer[StageConfig]
    output: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, stage: _Optional[_Iterable[_Union[StageConfig, _Mapping]]] = ..., output: _Optional[_Iterable[str]] = ...) -> None: ...
