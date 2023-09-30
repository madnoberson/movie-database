from typing_extensions import TypedDict
from dataclasses import dataclass


class Data(TypedDict):

    username_exists: bool


@dataclass(frozen=True, slots=True)
class CheckUsernameExists:
    
    data: Data