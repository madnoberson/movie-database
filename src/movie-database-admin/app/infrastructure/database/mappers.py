from typing import Mapping, Type, Any

from pydantic import TypeAdapter

from app.domain.models.model import ModelT


def as_domain_model(model: Type[ModelT], mapping: Mapping[str, Any]) -> ModelT:
    """
    Converts `mapping` into `model` and returns it. Ignores all fields that
    don't belong to to `model`
    """
    return TypeAdapter(model).validate_python(dict(mapping))
    