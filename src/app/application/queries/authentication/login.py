from dataclasses import dataclass
from typing import NewType

from app.application.common.handler import QueryHandler
from app.application.common.exceptions import user as user_exceptions
from app.application.common.interfaces.readers import AuthenticationReader
from app.application.common.query_results.authentication.login import Data


@dataclass(frozen=True, slots=True)
class InputDTO:

    username: str
    password: str


OutputDTO = NewType("OutputDTO", Data)


class Login(QueryHandler):

    def __init__(self, auth_reader: AuthenticationReader) -> None:
        self.auth_reader = auth_reader

    async def __call__(self, data: InputDTO) -> OutputDTO:
        ...