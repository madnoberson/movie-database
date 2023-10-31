from dataclasses import dataclass
from uuid import UUID

from app.application.common.interfaces.uow import UnitOfWork
from app.application.common.interfaces import repositories
from app.application.common.exceptions import user as user_exceptions
from app.application.commands.handler import CommandHandler


@dataclass(frozen=True, slots=True)
class InputDTO:

    user_id: UUID
    new_username: str


class EnsureUsernameChange(CommandHandler):

    def __init__(
        self,
        user_repo: repositories.UserRepository,
        uow: UnitOfWork
    ) -> None:
        self.user_repo = user_repo
        self.uow = uow
    
    async def __call__(self, data: InputDTO) -> None:
        # 1.Get user
        user = await self.user_repo.get_user(user_id=data.user_id)
        if user is None:
            raise user_exceptions.UserDoesNotExistError()
        
        # 2.Change username
        user.change_username(username=data.new_username)
        await self.user_repo.update_user(user)

        await self.uow.commit()