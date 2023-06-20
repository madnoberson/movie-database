from dataclasses import dataclass
from typing import Generic, TypeVar


V = TypeVar("V")
E = TypeVar("E")


@dataclass(frozen=True, slots=True, match_args=True)
class Result(Generic[V, E]):

    value: V | None
    error: E | None

