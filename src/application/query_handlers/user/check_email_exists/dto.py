from dataclasses import dataclass
from typing import NewType

from src.application.common.query_results.user.check_email_exists import Data


@dataclass(frozen=True, slots=True)
class CheckEmailExistsDTO:

    email: str


CheckEmailExistsResultDTO = NewType("CheckEmailExistsResultDTO", Data)