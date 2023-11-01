from typing import Mapping, Type, Any

from pydantic import TypeAdapter

from app.domain.models.model import ModelT
from app.application.common.query_results.query_result import QueryResultT


def as_domain_model(model: Type[ModelT], mapping: Mapping[str, Any]) -> ModelT:
    """
    Converts `mapping` into `model` and returns it. Ignores all fields that
    don't belong to to `model`
    """
    return TypeAdapter(model).validate_python(dict(mapping))


def as_query_result(query_result: Type[QueryResultT], mapping: Mapping[str, Any]) -> QueryResultT:
    """
    Converts `mapping` into `query_result` and returns it. Ignores all fields that
    don't belong to to `query_model`
    """
    return TypeAdapter(query_result).validate_python(dict(mapping))