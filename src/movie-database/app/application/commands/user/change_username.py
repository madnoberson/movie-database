from dataclasses import dataclass

from app.application.common.interfaces.identity_provider import IdentityProvider
from app.application.common.interfaces.uow import UnitOfWork
from app.application.common.interfaces import repositories
from app.application.common.exceptions import auth as auth_exceptions
from app.application.commands.handler import CommandHandler


@dataclass(frozen=True, slots=True)
class InputDTO:

    username: str


class ChangeUsername(CommandHandler):

    def __init__(
        self,
        user_repo: repositories.UserRepository,
        identity_provider: IdentityProvider,
        uow: UnitOfWork
    ) -> None:
        self.user_repo = user_repo
        self.identity_provider = identity_provider
        self.uow = uow
    
    async def __call__(self, data: InputDTO) -> None:
        # 1.Get current user id
        current_user_id = await self.identity_provider.get_current_user_id()
        if current_user_id is None:
            raise auth_exceptions.UnauthorizedError()
        
        # 2.Get user and change username
        user = await self.user_repo.get_user(user_id=current_user_id)
        user.change_username(username=data.username)

        await self.user_repo.update_user(user)
        await self.uow.commit()