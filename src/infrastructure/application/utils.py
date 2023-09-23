from typing import Sequence, Mapping, Type, Any, get_args, get_origin
from datetime import datetime
from enum import IntEnum
from uuid import UUID


def adapt(value: Any, type: Any) -> Any:
    """
    Casts `value` to `type` if possible, otherwise raises `ValueError`.
    Supports: cast `bytes` | `str` to `UUID`, cast `str` | `int` | `float` to `datetime`,
    cast `str` | `int` to `bool`, cast `str | int` to `IntEnum`,
    cast `list[str | int]` to `list[IntEnum]`.

    Adheres to some non-standard rules. List of rules:

    * If `type` is `bool`, `value` is `str` and equals to `'0'` or `'1'`,
    casting will work as if `value` were `0` or `1`. Thus, with `value` equal
    to `'0'`, the output value would be `False`, and with `value` equal to `'1'`
    the output value would be `True`
    """

    def cast_to_uuid(_value: str | bytes) -> UUID:
        if isinstance(_value, str): return UUID(hex=_value)
        elif isinstance(_value, bytes): return UUID(bytes=_value)
        raise ValueError
    
    def cast_to_datetime(_value: str | int | float) -> datetime:
        if isinstance(_value, str): return datetime.fromisoformat(_value)
        elif  isinstance(_value, int): return datetime.fromordinal(_value)
        elif isinstance(_value, float): return datetime.fromtimestamp(_value)
        raise ValueError
    
    def cast_to_bool(_value: str | int | None) -> bool:
        if isinstance(_value, str) and _value in ("0", "1"): return bool(int(_value))
        elif isinstance(_value, (str, int)): return bool(_value)
        elif _value is None: return False
        raise ValueError

    def cast_to_int_enum(_value: Sequence[str | int], int_enum: Type[IntEnum]) -> IntEnum:
        if not issubclass(int_enum, IntEnum): raise ValueError
        return int_enum(int(_value))

    def cast_to_list_of_int_enums(_value: Sequence[str | int], int_enum: Type[IntEnum]) -> list[IntEnum]:
        if not isinstance(_value, Sequence) and not issubclass(int_enum, IntEnum): raise ValueError
        return list(map(lambda el: int_enum(int(el)), _value))

    def check_type_is_list_of_int_enums(_type: Any) -> bool:
        return (
            (origin := get_origin(_type)) is not None and origin == list and
            (args := get_args(_type)) and issubclass(args[0], IntEnum)
        )

    type_args = get_args(type)
    is_optional = False
    if len(type_args) == 2 and None in type_args:
        is_optional = True
        type_args = list(type_args)
        type_args.remove(None)
        type = type_args[0]
    elif len(type_args) >= 2: raise ValueError

    if value is None and is_optional: return None
    elif type == UUID: return cast_to_uuid(value)
    elif type == datetime: return cast_to_datetime(value)
    elif type == bool: return cast_to_bool(value)
    elif issubclass(type, IntEnum): return cast_to_int_enum(value, type)
    elif check_type_is_list_of_int_enums(type): return cast_to_list_of_int_enums(value, get_args(type)[0])
    raise ValueError


DomainModel = object


def as_domain_model(
    model: Type[DomainModel], mapping: Mapping[str, Any]
) -> DomainModel:
    model_data = {}
    for key, value in mapping.items():
        if key not in model.__annotations__:
            continue
        elif type(value) == model.__annotations__[key]:
            model_data.update({key: value})
        else:
            adapted_value = adapt(value, model.__annotations__[key])
            model_data.update({key: adapted_value})
    return model(**model_data)


QueryResult = object


def as_query_result(
    query_result: Type[QueryResult], mapping: Mapping[str, Any]
) -> QueryResult:
    ...
