from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True, slots=True)
class RegisterCommand:

    username: str
    password: str


@dataclass(frozen=True, slots=True)
class RegisterCommandResult:

    user_id: UUID
