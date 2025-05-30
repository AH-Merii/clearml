"""Parsers to change model structure into different ones."""
import inspect
from typing import Optional, Union, Any

from . import fields, builders, errors


def to_struct(model: Any) -> dict:
    """Cast instance of model to python structure.

    :param model: Model to be casted.
    :rtype: ``dict``

    """
    model.validate()

    resp = {}
    for _, name, field in model.iterate_with_name():
        value = field.__get__(model)
        if value is None:
            continue

        value = field.to_struct(value)
        resp[name] = value
    return resp


def to_json_schema(cls) -> dict:
    """Generate JSON schema for given class.

    :param cls: Class to be casted.
    :rtype: ``dict``

    """
    builder = build_json_schema(cls)
    return builder.build()


def build_json_schema(
    value: Any,
    parent_builder: Optional[Union[builders.ObjectBuilder, builders.PrimitiveBuilder]] = None,
) -> Union[builders.ObjectBuilder, builders.PrimitiveBuilder]:
    from .models import Base

    cls = value if inspect.isclass(value) else value.__class__
    if issubclass(cls, Base):
        return build_json_schema_object(cls, parent_builder)
    else:
        return build_json_schema_primitive(cls, parent_builder)


def build_json_schema_object(cls, parent_builder: builders.Builder = None) -> builders.ObjectBuilder:
    builder = builders.ObjectBuilder(cls, parent_builder)
    if builder.count_type(builder.type) > 1:
        return builder
    for _, name, field in cls.iterate_with_name():
        if isinstance(field, fields.EmbeddedField):
            builder.add_field(name, field, _parse_embedded(field, builder))
        elif isinstance(field, fields.ListField):
            builder.add_field(name, field, _parse_list(field, builder))
        else:
            builder.add_field(name, field, _create_primitive_field_schema(field))
    return builder


def _parse_list(field: fields.ListField, parent_builder: builders.Builder) -> builders.ListBuilder:
    builder = builders.ListBuilder(parent_builder, field.nullable, default=field.default)
    for type in field.items_types:
        builder.add_type_schema(build_json_schema(type, builder))
    return builder


def _parse_embedded(field: fields.EmbeddedField, parent_builder: builders.Builder) -> builders.EmbeddedBuilder:
    builder = builders.EmbeddedBuilder(parent_builder, field.nullable, default=field.default)
    for type in field.types:
        builder.add_type_schema(build_json_schema(type, builder))
    return builder


def build_json_schema_primitive(cls, parent_builder: builders.Builder) -> builders.PrimitiveBuilder:
    builder = builders.PrimitiveBuilder(cls, parent_builder)
    return builder


def _create_primitive_field_schema(
    field: Union[fields.StringField, fields.IntField, fields.FloatField, fields.BoolField]
) -> dict:
    if isinstance(field, fields.StringField):
        obj_type = "string"
    elif isinstance(field, fields.IntField):
        obj_type = "number"
    elif isinstance(field, fields.FloatField):
        obj_type = "float"
    elif isinstance(field, fields.BoolField):
        obj_type = "boolean"
    else:
        raise errors.FieldNotSupported("Field {field} is not supported!".format(field=type(field).__class__.__name__))

    if field.nullable:
        obj_type = [obj_type, "null"]

    schema = {"type": obj_type}

    if field.has_default:
        schema["default"] = field._default

    return schema
