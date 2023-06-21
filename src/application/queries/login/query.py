from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True, slots=True)
class LoginQuery:

    username: str
    password: str


@dataclass(frozen=True, slots=True)
class LoginQueryResult:

    user_id: UUID
    