from dataclasses import dataclass
from typing import TypedDict


class Data(TypedDict):

    username_exists: bool


@dataclass(frozen=True, slots=True)
class CheckUsernameExists:
    
    data: Data
    extra: None