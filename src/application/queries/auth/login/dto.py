from dataclasses import dataclass
from typing import NewType

from src.application.common.query_results.auth.login import Data


@dataclass(frozen=True, slots=True)
class LoginDTO:

    username: str
    password: str


LoginResultDTO = NewType("LoginResultDTO", Data)
