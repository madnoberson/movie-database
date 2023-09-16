from typing import Mapping, Type, Union, Any

from src.domain.base import DomainModel
from .adaptation import adapt


__all__ = ["as_domain_model"]


def as_domain_model(model: Type[DomainModel], mapping: Mapping[str, Any]) -> DomainModel:
    """
    Converts `mapping` into `model`.
    
    1) Model must have only one type for each field, except optional `None`.
    Thus, `field: str | None` will work fine, but `field: bool | int`
    will raise `ValueError`.
    2) Model must not have default values for fields, otherwise func will raise `ValueError`

    Supports: cast `bytes` | `str` to `UUID`, cast `str` | `int` | `float` to `datetime`,
    cast `str` | `int` to `bool`, cast `list[str | int]` to `list[IntEnum]`.
    """ 

    def get_field_type_from_union(union: Union[Any, None]) -> Any | None:
        """Returns type from `union`, that is not `None`"""
        return list(filter(lambda e: not isinstance(None, e), union.__args__))[0]

    model_annotations = model.__annotations__
    model_data = {}
    for key, value in mapping.items():
        if key not in model_annotations:
            continue
        elif model_annotations[key] == type(value):
            model_data.update({key: value})
        elif len(model_annotations[key].__args__) == 1:
            adapted_value = adapt(value, model_annotations[key]) 
            model_data.update({key: adapted_value})
        elif len(model_annotations[key].__args__) == 2:
            type = get_field_type_from_union(model_annotations[key])
            adapted_value = adapt(value, type)
            model_data.update({key: adapted_value})
    
    if len(model_data) == len(model_annotations):
        raise ValueError
    
    return model(**model_data)
