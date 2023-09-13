from typing import Type, Mapping, Any, Sequence
from dataclasses import make_dataclass, field
from datetime import datetime
from enum import IntEnum
from uuid import UUID

from src.application.common.query_results.base import QueryResult


__all__ = ["as_domain_model", "ensure_args"]


DomainModel = object


def as_domain_model(
    model: Type[DomainModel], mapping: Mapping[str, Any]
) -> DomainModel:
    """
    Converts `mapping` into `model`.

    Supports:
    * Converting `str` into `UUID`
    * Converting `list[str | int]` into `IntEnum`
    * Converting `str` into `datetime`
    """ 
    model_annotations = model.__annotations__
    model_data = {}
    for key, value in mapping.items():
        if key not in model_annotations:
            continue
        if model_annotations[key] == type(value):
            model_data.update({key: value})
            continue
        adapted_value = adapt(value, model_annotations[key])
        model_data.update({key: adapted_value})
    
    return model(**model_data)


def as_query_result(
    query_result: Type[QueryResult], mapping: Mapping[str, Any]
) -> QueryResult:
    query_result_annotations = query_result.__annotations__
    mapping_data, mapping_extra = mapping["data"], mapping.get("extra")

    query_result_data = query_result_annotations.get("data")
    query_result_data_annotations = query_result_data.__annotations__
    data = {}
    for key, value in mapping_data.items():
        if key not in query_result_data_annotations.keys():
            continue
        if query_result_data_annotations[key] == type(value):  
            data.update({key: value})
            continue
        adapted_value = adapt(value, query_result_data_annotations[key])
        data.update({key: adapted_value})
    
    query_result_extra = query_result_annotations.get("extra")
    if query_result_extra is None:
        return query_result(data=data, extra=None)

    assert mapping_extra is not None
    query_result_extra_annotations = query_result_data.__annotations__
    fields = []
    for key, value in mapping_extra.items():
        if key not in query_result_extra_annotations.keys():
            continue
        if query_result_extra_annotations[key] == type(value):
            fields.append((key, type(value), value))
            continue
        adapted_value = adapted_value(value, query_result_extra_annotations[key])
        fields.append((key, query_result_extra_annotations[key], value))

    return query_result(data=data, extra=make_dataclass("Data", fields=fields))


def ensure_args(*args) -> None:
    """Ensures that only one arg from `args` is not `None`"""
    assert args.count(None) == len(args) - 1


def adapt(value: Any, type: Any) -> Any:
    if type == UUID:
        assert isinstance(value, str)
        return UUID(value)
    elif type == datetime:
        assert isinstance(value, str)
        return datetime.fromisoformat(value)
    else:
        assert isinstance(value, Sequence)
        list_el_cls = type.__args__[0]
        assert issubclass(list_el_cls, IntEnum)
        return list(map(lambda el: list_el_cls(int(el)), value))
    