import importlib.util
import os
import sys

from google.protobuf.descriptor import FieldDescriptor

# Map for field types
TYPE_MAP = {
    FieldDescriptor.TYPE_DOUBLE: "double",
    FieldDescriptor.TYPE_FLOAT: "float",
    FieldDescriptor.TYPE_INT64: "int64",
    FieldDescriptor.TYPE_UINT64: "uint64",
    FieldDescriptor.TYPE_INT32: "int32",
    FieldDescriptor.TYPE_FIXED64: "fixed64",
    FieldDescriptor.TYPE_FIXED32: "fixed32",
    FieldDescriptor.TYPE_BOOL: "bool",
    FieldDescriptor.TYPE_STRING: "string",
    FieldDescriptor.TYPE_GROUP: "group",
    FieldDescriptor.TYPE_MESSAGE: "message",
    FieldDescriptor.TYPE_BYTES: "bytes",
    FieldDescriptor.TYPE_UINT32: "uint32",
    FieldDescriptor.TYPE_ENUM: "enum",
    FieldDescriptor.TYPE_SFIXED32: "sfixed32",
    FieldDescriptor.TYPE_SFIXED64: "sfixed64",
    FieldDescriptor.TYPE_SINT32: "sint32",
    FieldDescriptor.TYPE_SINT64: "sint64",
}


def get_type_name(field):
    if field.type == FieldDescriptor.TYPE_MESSAGE:
        return field.message_type.full_name
    if field.type == FieldDescriptor.TYPE_ENUM:
        return field.enum_type.full_name
    return TYPE_MAP.get(field.type, "unknown")


def format_default_value(field):
    val = field.default_value
    if field.type == FieldDescriptor.TYPE_STRING:
        return f'"{val}"'
    if field.type == FieldDescriptor.TYPE_BYTES:
        # Best effort for bytes
        return f'"{val}"'
    if field.type == FieldDescriptor.TYPE_BOOL:
        return "true" if val else "false"
    if field.type == FieldDescriptor.TYPE_ENUM:
        # default_value is int for enum in python descriptor.
        # We need to find the name.
        if isinstance(val, int):
            # values_by_number returns EnumValueDescriptor
            if val in field.enum_type.values_by_number:
                return field.enum_type.values_by_number[val].name
            return str(val)  # Fallback
    return str(val)


def print_enum(enum_desc, indent_level=0):
    indent = "  " * indent_level
    lines = []
    lines.append(f"{indent}enum {enum_desc.name} {{")
    for value in enum_desc.values:
        lines.append(f"{indent}  {value.name} = {value.number};")
    lines.append(f"{indent}}}")
    return "\n".join(lines)


def print_message(msg_desc, indent_level=0):
    indent = "  " * indent_level
    lines = []
    lines.append(f"{indent}message {msg_desc.name} {{")

    for enum in msg_desc.enum_types:
        lines.append(print_enum(enum, indent_level + 1))

    for nested in msg_desc.nested_types:
        lines.append(print_message(nested, indent_level + 1))

    for field in msg_desc.fields:
        # Label
        label = ""
        if field.label == FieldDescriptor.LABEL_OPTIONAL:
            label = "optional "
        elif field.label == FieldDescriptor.LABEL_REQUIRED:
            label = "required "
        elif field.label == FieldDescriptor.LABEL_REPEATED:
            label = "repeated "

        # Type
        type_name = get_type_name(field)

        line = f"{indent}  {label}{type_name} {field.name} = {field.number}"

        # Default value
        if field.has_default_value:
            default_str = format_default_value(field)
            line += f" [