from typing import Any, Sequence
from datetime import datetime
from enum import IntEnum
from uuid import UUID


__all__ = ["adapt"]


def adapt(_value: Any, type: Any) -> Any:
    """
    Casts `value` to `type` if possible, otherwise raises `ValueError`.
    Supports: cast `bytes` | `str` to `UUID`, cast `str` | `int` | `float` to `datetime`,
    cast `str` | `int` to `bool`, cast `list[str | int]` to `list[IntEnum]`.

    Adheres to some non-standard rules. List of rules:

    * If `type` is `bool`, `value` is `str` and equals to `'0'` or `'1'`,
    casting will work as if `value` were `0` or `1`. Thus, with `value` equal
    to `'0'`, the output value would be `False`, and with `value` equal to `'1'`
    the output value would be `True`
    """

    def cast_to_uuid(value: str | bytes) -> UUID:
        is_bytes = isinstance(value, bytes)
        if is_bytes: return UUID(bytes=value)
        is_str = isinstance(value, str)
        if is_str: return UUID(hex=value)
        raise ValueError
    
    def cast_to_datetime(value: str | int | float) -> datetime:
        is_str = isinstance(value, str)
        if is_str: return datetime.fromisoformat(value)
        is_int = isinstance(value, int)
        if is_int: return datetime.fromordinal(value)
        is_float = isinstance(value, float)
        if is_float: return datetime.fromtimestamp(value)
        raise ValueError
    
    def cast_to_bool(value: str | int) -> bool:
        is_str = isinstance(value, str)
        if is_str and value in ("0", "1"): return bool(int(value))
        elif is_str: return bool(str)
        is_int = isinstance(value, int)
        if is_int: return bool(value)
        if value is None: return False
        raise ValueError
    
    def cast_to_list_of_int_enums(value: Sequence[str | int], int_enum: IntEnum) -> list[IntEnum]:
        is_sequence = isinstance(value, Sequence)
        if not is_sequence: return None
        is_int_enum = issubclass(int_enum, IntEnum)
        if is_int_enum: return list(map(lambda el: int_enum(int(el)), value))
        raise ValueError
    
    def check_type_is_list_of_int_enums(type: Any) -> bool:
        return (
            hasattr(type, "__origin__") and type.__origin__ == list and
            len(type.__args__) == 1 and issubclass(type.__args__[0], IntEnum)
        )
    
    if type == UUID: return cast_to_uuid(_value)
    elif type == datetime: return cast_to_datetime(_value)
    elif type == bool: return cast_to_bool(_value)
    elif check_type_is_list_of_int_enums(type):
        return cast_to_list_of_int_enums(_value, type.__args__[0])
    else: raise ValueError

