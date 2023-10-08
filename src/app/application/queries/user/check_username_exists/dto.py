from dataclasses import dataclass
from typing import NewType

from app.application.common.query_results.user.check_username_exists import Data


@dataclass(frozen=True, slots=True)
class CheckUsernameExistsDTO:

    username: str


CheckUsernameExistsResultDTO = NewType("CheckUsernameExistsResultDTO", Data)