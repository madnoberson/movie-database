from typing import NewType

from app.application.common.handler import QueryHandler
from app.application.common.exceptions import user as user_exceptions
from app.application.common.exceptions import authentication as auth_exceptions
from app.application.common.interfaces.readers import UserReader
from app.application.common.interfaces.identity_provider import IdentityProvider
from app.application.common.query_results.user.get_current_user import Data


OutputDTO = NewType("OutputDTO", Data)


class GetCurrentUser(QueryHandler):

    def __init__(
        self,
        user_reader: UserReader,
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
        if query_result is None:
            raise user_exceptions.UserDoesNotExistError()
        
        return OutputDTO(query_result.data)
        