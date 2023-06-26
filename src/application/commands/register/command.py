from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True, slots=True)
class RegisterCommand:

    username: str
    password: str

    def __post_init__(self) -> None:
        is_valid = (
            isinstance(self.username, str) and
            len(self.username) > 0 and
            isinstance(self.password, str) and
            len(self.password) >= 6
        )
        if not is_valid:
            raise ValueError()


@dataclass(frozen=True, slots=True)
class RegisterCommandResult:

    user_id: UUID
