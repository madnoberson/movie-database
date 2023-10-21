from dataclasses import dataclass
from typing import NewType

from app.application.common.query_results.auth.login import Data
from app.application.common.interfaces import readers
from app.application.common.exceptions import user as user_exceptions
from app.application.common.exceptions import auth as auth_exceptions
from app.application.queries.handler import QueryHandler


@dataclass(frozen=True, slots=True)
class InputDTO:

    username: str
    password: str


OutputDTO = NewType("OutputDTO", Data)


class Login(QueryHandler):

    def __init__(self, auth_reader: readers.AuthReader) -> None:
        self.auth_reader = auth_reader

    async def __call__(self, data: InputDTO) -> OutputDTO:
        # 1.Get query result
        query_result = await self.auth_reader.login(username=data.username)
        if query_result is None:
            raise user_exceptions.UserDoesNotExistError()

        # 2.Ensure password is correct
        if query_result.extra.password != data.password:
            raise auth_exceptions.PasswordIsNotCorrectError()
        
        return query_result.data
