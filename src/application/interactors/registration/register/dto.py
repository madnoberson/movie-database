from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True, slots=True)
class RegisterDTO:

    username: str
    password: str


@dataclass(frozen=True, slots=True)
class RegisterResultDTO:

    user_id: UUID