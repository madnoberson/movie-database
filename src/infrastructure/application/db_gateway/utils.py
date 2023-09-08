from typing import Type, Mapping, Any, Sequence
from datetime import datetime
from enum import IntEnum
from uuid import UUID


__all__ = ["as_domain_model"]


DomainModel = object


def as_domain_model(
    model: Type[DomainModel], mapping: Mapping[str, Any]
) -> DomainModel:
    """
    ### Summary:
        * Converts `mapping` into `model`.
    ### Supports:
        * Converting `str` into `UUID`
        * Converting `list[str | int]` into `IntEnum`
        * Converting `str` into `datetime`
    """
    model_annotations = model.__annotations__
    model_data = {}
    for key, value in mapping.items():
        if key not in model_annotations:
            continue
        if type(model_annotations[key]) == type(value):
            continue
        adapted_value = _adapt(value, model_annotations[key])
        model_data.update(**{key: adapted_value})
    
    return model(**model_data)


def _adapt(value: Any, type: Any) -> Any:
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
    