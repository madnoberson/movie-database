from abc import ABC, abstractmethod
from typing import TypedDict


class QueryResult(ABC):

    data: TypedDict
    extra: object | None
