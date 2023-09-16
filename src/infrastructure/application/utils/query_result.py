from typing import Mapping, Type, Union, Any
from dataclasses import make_dataclass

from src.application.common.query_results.base import QueryResult
from .adaptation import adapt


__all__ = ["as_query_result"]


def as_query_result(
    query_result: Type[QueryResult], mapping: Mapping[str, Any]
) -> QueryResult:
    
    def get_field_type_from_union(union: Union[Any, None]) -> Any | None:
        """Returns type from `union`, that is not `None`"""
        return list(filter(lambda e: not isinstance(None, e), union.__args__))[0]

    def as_query_result_data(
        annotations: dict[str ,Any], _mapping: Mapping[str, Any]
    ) -> dict[str, Any]:
        data = {}
        for key, value in _mapping.items():
            if key not in annotations.keys():
                continue
            elif annotations[key] == type(value):
                data.update({key: value})
            elif len(annotations[key].__args__) == 1:
                adapted_value = adapt(value, annotations[key])
                data.update({key: adapted_value})
            elif len(annotations[key].__args__) == 2:
                type = get_field_type_from_union(annotations[key])
                adapted_value = adapt(value, type)
                data.update({key: adapted_value})

        if len(data) == len(annotations):
            raise ValueError
        
        return data
            
    def as_query_result_extra(
        annotations: dict[str, Any], _mapping: Mapping[str, Any]
    ) -> object:
        fields = []
        for key, value in _mapping.items():
            if key not in annotations.keys():
                continue
            elif annotations[key] == type(value):
                fields.append((key, annotations[key], value))
            elif len(annotations[key].__args__) == 1:
                adapted_value = adapt(value, annotations[key])
                data.update({key: adapted_value})
            elif len(annotations[key].__args__) == 2:
                type = get_field_type_from_union(annotations[key])
                adapted_value = adapt(value, type)
                data.update({key: adapted_value})


    query_result_annotations = query_result.__annotations__
    mapping_data, mapping_extra = mapping["data"], mapping.get("extra")
    print(mapping_data, mapping_extra)

    query_result_data = query_result_annotations.get("data")
    query_result_data_annotations = query_result_data.__annotations__
    print(query_result_annotations)
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
    print(query_result_extra_annotations)
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