from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class CheckUsernameExistenceQuery:
    
    username: str

    def __post_init__(self) -> None:
        is_valid = (
            isinstance(self.username, str) and
            len(self.username) > 0
        )
        if not is_valid:
            raise ValueError


@dataclass(frozen=True, slots=True)
class CheckUsernameExistenceQueryResult:

    exists: bool