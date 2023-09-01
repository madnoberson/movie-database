from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True, slots=True)
class CreateUserDTO:

    email: str
    password: str


@dataclass(frozen=True, slots=True)
class CreateUserResultDTO:

    user_id: UUID