from dataclasses import dataclass
from typing import TypedDict

from src.application.common.query_results.base import QueryResult


class Data(TypedDict):

    email_exists: bool


@dataclass(frozen=True, slots=True)
class CheckEmailExists(QueryResult):

    data: Data
    extra: None