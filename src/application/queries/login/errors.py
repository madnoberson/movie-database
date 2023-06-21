from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class UsernameDoesNotExistError(Exception):

    username: str


@dataclass(frozen=True, slots=True)
class PasswordIsIncorrectError(Exception):
    ...