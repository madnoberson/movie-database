from typing import NewType

from app.application.common.query_results.user.get_current_user import Data
from app.application.common.interfaces.identity_provider import IdentityProvider
from app.application.common.interfaces import readers
from app.application.common.exceptions import auth as auth_exceptions
from app.application.queries.handler import QueryHandler


OutputDTO = NewType("OutputDTO", Data)


class GetCurrentUser(QueryHandler):

    def __init__(
        self,
        user_reader: readers.UserReader,
        identity_provider: IdentityProvider
    ) -> None:
        self.user_reader = user_reader
        self.identity_provider = identity_provider

    async def __call__(self) -> OutputDTO:
        # 1.Get current user id
        current_user_id = await self.identity_provider.get_current_user_id()
        if current_user_id is None:
            raise auth_exceptions.UnauthorizedError()

        # 2.Get query result
        query_result = await self.user_reader.get_current_user(user_id=current_user_id)
        
        return OutputDTO(query_result.data)
        