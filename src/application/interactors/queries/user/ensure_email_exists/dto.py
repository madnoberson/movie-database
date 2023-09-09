from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class EnsureEmailExistsDTO:

    email: str


@dataclass(frozen=True, slots=True)
class EnsureEmailExistsResultDTO:

    email_exists: bool