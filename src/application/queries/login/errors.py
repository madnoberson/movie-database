from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class UsernameDoesNotExistError(Exception):

    username: str

    @property
    def message(self) -> str:
        return f"Username doesn't exist"


@dataclass(frozen=True, slots=True)
class PasswordIsIncorrectError(Exception):
    
    @property
    def message(self) -> str:
        return f"Incorrect password"