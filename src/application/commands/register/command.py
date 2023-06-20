from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class RegisterCommand:

    username: str
    password: str
    