from dataclasses import dataclass
from typing import TypedDict

from src.application.common.query_results.base import QueryResult


class Data(TypedDict):

    username_exists: bool


@dataclass(frozen=True, slots=True)
class CheckUsernameExists(QueryResult):

    data: Data
    extra: None