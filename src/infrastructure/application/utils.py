from typing import Mapping, Type, TypeVar, Any

from pydantic import TypeAdapter


DM = TypeVar("DM")


def as_domain_model(model: Type[DM], mapping: Mapping[str, Any]) -> DM:
    return TypeAdapter(model).validate_python(mapping)
    

QR = TypeVar("QR")


def as_query_result(query_result: Type[QR], mapping: Mapping[str, Any]) -> QR:
    return TypeAdapter(query_result).validate_python(mapping)