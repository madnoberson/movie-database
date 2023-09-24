from typing_extensions import TypedDict
from dataclasses import dataclass
from uuid import UUID


class Data(TypedDict):
    
    user_id: UUID


@dataclass(frozen=True, slots=True)
class Extra:

    encoded_password: str


@dataclass(frozen=True, slots=True)
class Login:

    data: Data
    extra: Extra