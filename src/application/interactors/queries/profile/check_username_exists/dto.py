from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class CheckUsernameExistsDTO:

    username: str


@dataclass(frozen=True, slots=True)
class CheckUsernameExistsResultDTO:

    username_exists: bool