from dataclasses import dataclass
from uuid import UUID

from app.application.common.query_results.query_result import QueryResult


@dataclass(frozen=True, slots=True)
class Data:

    user_id: UUID


@dataclass(frozen=True, slots=True)
class Extra:

    password: str


@dataclass(frozen=True, slots=True)
class Login(QueryResult):

    data: Data
    extra: Extra

