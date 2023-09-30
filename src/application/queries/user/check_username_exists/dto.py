from dataclasses import dataclass
from typing import NewType

from src.application.common.query_results.user.check_username_exists import Data


@dataclass(frozen=True, slots=True)
class CheckUsernameExistsDTO:

    username: str


CheckUsernameExistsResultDTO = NewType("CheckUsernameExistsResultDTO", Data)