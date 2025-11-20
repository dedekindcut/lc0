from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class TensorProto(_message.Message):
    __slots__ = ("dims", "data_type", "name", "raw_data", "doc_string", "external_data", "data_location")
    class DataType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        UNDEFINED: _ClassVar[TensorProto.DataType]
        FLOAT: _ClassVar[TensorProto.DataType]
        UINT8: _ClassVar[TensorProto.DataType]
        INT8: _ClassVar[TensorProto.DataType]
        UINT16: _ClassVar[TensorProto.DataType]
        INT16: _ClassVar[TensorProto.DataType]
        INT32: _ClassVar[TensorProto.DataType]
        INT64: _ClassVar[TensorProto.DataType]
        STRING: _ClassVar[TensorProto.DataType]
        BOOL: _ClassVar[TensorProto.DataType]
        FLOAT16: _ClassVar[TensorProto.DataType]
        DOUBLE: _ClassVar[TensorProto.DataType]
        UINT32: _ClassVar[TensorProto.DataType]
        UINT64: _ClassVar[TensorProto.DataType]
        COMPLEX64: _ClassVar[TensorProto.DataType]
        COMPLEX128: _ClassVar[TensorProto.DataType]
        BFLOAT16: _ClassVar[TensorProto.DataType]
        FLOAT8E4M3FN: _ClassVar[TensorProto.DataType]
        FLOAT8E4M3FNUZ: _ClassVar[TensorProto.DataType]
        FLOAT8E5M2: _ClassVar[TensorProto.DataType]
        FLOAT8E5M2FNUZ: _ClassVar[TensorProto.DataType]
    UNDEFINED: TensorProto.DataType
    FLOAT: TensorProto.DataType
    UINT8: TensorProto.DataType
    INT8: TensorProto.DataType
    UINT16: TensorProto.DataType
    INT16: TensorProto.DataType
    INT32: TensorProto.DataType
    INT64: TensorProto.DataType
    STRING: TensorProto.DataType
    BOOL: TensorProto.DataType
    FLOAT16: TensorProto.DataType
    DOUBLE: TensorProto.DataType
    UINT32: TensorProto.DataType
    UINT64: TensorProto.DataType
    COMPLEX64: TensorProto.DataType
    COMPLEX128: TensorProto.DataType
    BFLOAT16: TensorProto.DataType
    FLOAT8E4M3FN: TensorProto.DataType
    FLOAT8E4M3FNUZ: TensorProto.DataType
    FLOAT8E5M2: TensorProto.DataType
    FLOAT8E5M2FNUZ: TensorProto.DataType
    class DataLocation(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        DEFAULT: _ClassVar[TensorProto.DataLocation]
        EXTERNAL: _ClassVar[TensorProto.DataLocation]
    DEFAULT: TensorProto.DataLocation
    EXTERNAL: TensorProto.DataLocation
    DIMS_FIELD_NUMBER: _ClassVar[int]
    DATA_TYPE_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    RAW_DATA_FIELD_NUMBER: _ClassVar[int]
    DOC_STRING_FIELD_NUMBER: _ClassVar[int]
    EXTERNAL_DATA_FIELD_NUMBER: _ClassVar[int]
    DATA_LOCATION_FIELD_NUMBER: _ClassVar[int]
    dims: _containers.RepeatedScalarFieldContainer[int]
    data_type: TensorProto.DataType
    name: str
    raw_data: bytes
    doc_string: str
    external_data: _containers.RepeatedCompositeFieldContainer[StringStringEntryProto]
    data_location: TensorProto.DataLocation
    def __init__(self, dims: _Optional[_Iterable[int]] = ..., data_type: _Optional[_Union[TensorProto.DataType, str]] = ..., name: _Optional[str] = ..., raw_data: _Optional[bytes] = ..., doc_string: _Optional[str] = ..., external_data: _Optional[_Iterable[_Union[StringStringEntryProto, _Mapping]]] = ..., data_location: _Optional[_Union[TensorProto.DataLocation, str]] = ...) -> None: ...

class StringStringEntryProto(_message.Message):
    __slots__ = ("key", "value")
    KEY_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    key: str
    value: str
    def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...

class AttributeProto(_message.Message):
    __slots__ = ("name", "doc_string", "f", "i", "s", "t", "floats", "ints", "strings", "tensors", "type")
    class AttributeType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        UNDEFINED: _ClassVar[AttributeProto.AttributeType]
        FLOAT: _ClassVar[AttributeProto.AttributeType]
        INT: _ClassVar[AttributeProto.AttributeType]
        STRING: _ClassVar[AttributeProto.AttributeType]
        TENSOR: _ClassVar[AttributeProto.AttributeType]
        FLOATS: _ClassVar[AttributeProto.AttributeType]
        INTS: _ClassVar[AttributeProto.AttributeType]
        STRINGS: _ClassVar[AttributeProto.AttributeType]
        TENSORS: _ClassVar[AttributeProto.AttributeType]
    UNDEFINED: AttributeProto.AttributeType
    FLOAT: AttributeProto.AttributeType
    INT: AttributeProto.AttributeType
    STRING: AttributeProto.AttributeType
    TENSOR: AttributeProto.AttributeType
    FLOATS: AttributeProto.AttributeType
    INTS: AttributeProto.AttributeType
    STRINGS: AttributeProto.AttributeType
    TENSORS: AttributeProto.AttributeType
    NAME_FIELD_NUMBER: _ClassVar[int]
    DOC_STRING_FIELD_NUMBER: _ClassVar[int]
    F_FIELD_NUMBER: _ClassVar[int]
    I_FIELD_NUMBER: _ClassVar[int]
    S_FIELD_NUMBER: _ClassVar[int]
    T_FIELD_NUMBER: _ClassVar[int]
    FLOATS_FIELD_NUMBER: _ClassVar[int]
    INTS_FIELD_NUMBER: _ClassVar[int]
    STRINGS_FIELD_NUMBER: _ClassVar[int]
    TENSORS_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    name: str
    doc_string: str
    f: float
    i: int
    s: bytes
    t: TensorProto
    floats: _containers.RepeatedScalarFieldContainer[float]
    ints: _containers.RepeatedScalarFieldContainer[int]
    strings: _containers.RepeatedScalarFieldContainer[bytes]
    tensors: _containers.RepeatedCompositeFieldContainer[TensorProto]
    type: AttributeProto.AttributeType
    def __init__(self, name: _Optional[str] = ..., doc_string: _Optional[str] = ..., f: _Optional[float] = ..., i: _Optional[int] = ..., s: _Optional[bytes] = ..., t: _Optional[_Union[TensorProto, _Mapping]] = ..., floats: _Optional[_Iterable[float]] = ..., ints: _Optional[_Iterable[int]] = ..., strings: _Optional[_Iterable[bytes]] = ..., tensors: _Optional[_Iterable[_Union[TensorProto, _Mapping]]] = ..., type: _Optional[_Union[AttributeProto.AttributeType, str]] = ...) -> None: ...

class NodeProto(_message.Message):
    __slots__ = ("input", "output", "name", "op_type", "attribute", "doc_string", "domain")
    INPUT_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    OP_TYPE_FIELD_NUMBER: _ClassVar[int]
    ATTRIBUTE_FIELD_NUMBER: _ClassVar[int]
    DOC_STRING_FIELD_NUMBER: _ClassVar[int]
    DOMAIN_FIELD_NUMBER: _ClassVar[int]
    input: _containers.RepeatedScalarFieldContainer[str]
    output: _containers.RepeatedScalarFieldContainer[str]
    name: str
    op_type: str
    attribute: _containers.RepeatedCompositeFieldContainer[AttributeProto]
    doc_string: str
    domain: str
    def __init__(self, input: _Optional[_Iterable[str]] = ..., output: _Optional[_Iterable[str]] = ..., name: _Optional[str] = ..., op_type: _Optional[str] = ..., attribute: _Optional[_Iterable[_Union[AttributeProto, _Mapping]]] = ..., doc_string: _Optional[str] = ..., domain: _Optional[str] = ...) -> None: ...

class TensorShapeProto(_message.Message):
    __slots__ = ("dim",)
    class Dimension(_message.Message):
        __slots__ = ("dim_value", "dim_param")
        DIM_VALUE_FIELD_NUMBER: _ClassVar[int]
        DIM_PARAM_FIELD_NUMBER: _ClassVar[int]
        dim_value: int
        dim_param: str
        def __init__(self, dim_value: _Optional[int] = ..., dim_param: _Optional[str] = ...) -> None: ...
    DIM_FIELD_NUMBER: _ClassVar[int]
    dim: _containers.RepeatedCompositeFieldContainer[TensorShapeProto.Dimension]
    def __init__(self, dim: _Optional[_Iterable[_Union[TensorShapeProto.Dimension, _Mapping]]] = ...) -> None: ...

class TypeProto(_message.Message):
    __slots__ = ("tensor_type",)
    class Tensor(_message.Message):
        __slots__ = ("elem_type", "shape")
        ELEM_TYPE_FIELD_NUMBER: _ClassVar[int]
        SHAPE_FIELD_NUMBER: _ClassVar[int]
        elem_type: TensorProto.DataType
        shape: TensorShapeProto
        def __init__(self, elem_type: _Optional[_Union[TensorProto.DataType, str]] = ..., shape: _Optional[_Union[TensorShapeProto, _Mapping]] = ...) -> None: ...
    TENSOR_TYPE_FIELD_NUMBER: _ClassVar[int]
    tensor_type: TypeProto.Tensor
    def __init__(self, tensor_type: _Optional[_Union[TypeProto.Tensor, _Mapping]] = ...) -> None: ...

class ValueInfoProto(_message.Message):
    __slots__ = ("name", "type", "doc_string")
    NAME_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    DOC_STRING_FIELD_NUMBER: _ClassVar[int]
    name: str
    type: TypeProto
    doc_string: str
    def __init__(self, name: _Optional[str] = ..., type: _Optional[_Union[TypeProto, _Mapping]] = ..., doc_string: _Optional[str] = ...) -> None: ...

class GraphProto(_message.Message):
    __slots__ = ("node", "name", "initializer", "doc_string", "input", "output")
    NODE_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    INITIALIZER_FIELD_NUMBER: _ClassVar[int]
    DOC_STRING_FIELD_NUMBER: _ClassVar[int]
    INPUT_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_FIELD_NUMBER: _ClassVar[int]
    node: _containers.RepeatedCompositeFieldContainer[NodeProto]
    name: str
    initializer: _containers.RepeatedCompositeFieldContainer[TensorProto]
    doc_string: str
    input: _containers.RepeatedCompositeFieldContainer[ValueInfoProto]
    output: _containers.RepeatedCompositeFieldContainer[ValueInfoProto]
    def __init__(self, node: _Optional[_Iterable[_Union[NodeProto, _Mapping]]] = ..., name: _Optional[str] = ..., initializer: _Optional[_Iterable[_Union[TensorProto, _Mapping]]] = ..., doc_string: _Optional[str] = ..., input: _Optional[_Iterable[_Union[ValueInfoProto, _Mapping]]] = ..., output: _Optional[_Iterable[_Union[ValueInfoProto, _Mapping]]] = ...) -> None: ...

class OperatorSetIdProto(_message.Message):
    __slots__ = ("domain", "version")
    DOMAIN_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    domain: str
    version: int
    def __init__(self, domain: _Optional[str] = ..., version: _Optional[int] = ...) -> None: ...

class ModelProto(_message.Message):
    __slots__ = ("ir_version", "producer_name", "producer_version", "domain", "model_version", "doc_string", "graph", "opset_import")
    IR_VERSION_FIELD_NUMBER: _ClassVar[int]
    PRODUCER_NAME_FIELD_NUMBER: _ClassVar[int]
    PRODUCER_VERSION_FIELD_NUMBER: _ClassVar[int]
    DOMAIN_FIELD_NUMBER: _ClassVar[int]
    MODEL_VERSION_FIELD_NUMBER: _ClassVar[int]
    DOC_STRING_FIELD_NUMBER: _ClassVar[int]
    GRAPH_FIELD_NUMBER: _ClassVar[int]
    OPSET_IMPORT_FIELD_NUMBER: _ClassVar[int]
    ir_version: int
    producer_name: str
    producer_version: str
    domain: str
    model_version: int
    doc_string: str
    graph: GraphProto
    opset_import: _containers.RepeatedCompositeFieldContainer[OperatorSetIdProto]
    def __init__(self, ir_version: _Optional[int] = ..., producer_name: _Optional[str] = ..., producer_version: _Optional[str] = ..., domain: _Optional[str] = ..., model_version: _Optional[int] = ..., doc_string: _Optional[str] = ..., graph: _Optional[_Union[GraphProto, _Mapping]] = ..., opset_import: _Optional[_Iterable[_Union[OperatorSetIdProto, _Mapping]]] = ...) -> None: ...
