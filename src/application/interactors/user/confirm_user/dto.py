from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ConfirmUserDTO:

    email: str