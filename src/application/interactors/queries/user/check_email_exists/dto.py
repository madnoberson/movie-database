from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class CheckEmailExistsDTO:

    email: str


@dataclass(frozen=True, slots=True)
class CheckEmailExistsResultDTO:

    email_exists: bool