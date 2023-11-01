from dataclasses import dataclass
from uuid import UUID

from app.domain.models.superuser import SuperUserPermissionEnum
from app.application.common.query_results.query_result import QueryResult


@dataclass(frozen=True, slots=True)
class Data:

    superuser_id: UUID
    permissions: list[SuperUserPermissionEnum]
    is_active: bool


@dataclass(frozen=True, slots=True)
class Extra:

    password: str


@dataclass(frozen=True, slots=True)
class Login(QueryResult):

    data: Data
    extra: Extra
