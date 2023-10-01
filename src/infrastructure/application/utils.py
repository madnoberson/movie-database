from typing import Mapping, Type, TypeVar, Any
from typing_extensions import TypedDict

from pydantic import TypeAdapter


DM = TypeVar("DM")


def as_domain_model(model: Type[DM], mapping: Mapping[str, Any]) -> DM:
    """
    Converts `mapping` into `model` and returns it. Ignores all fields that
    don't belong to to `model`
    """
    return TypeAdapter(model).validate_python(dict(mapping))
    

QR = TypeVar("QR", bound=TypedDict)


def as_query_result(query_result: Type[QR], mapping: Mapping[str, Any]) -> QR:
    """
    Converts `mapping` into `query_result` and returns it. Ignores all fields that
    don't belong to to `query_model`
    """
    return TypeAdapter(query_result).validate_python(dict(mapping))
