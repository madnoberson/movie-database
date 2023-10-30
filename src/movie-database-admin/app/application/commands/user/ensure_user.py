from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from app.domain.models.user import User
from app.application.common.interfaces.uow import UnitOfWork
from app.application.common.interfaces import repositories
from app.application.common.exceptions import user as user_exceptions
from app.application.commands.handler import CommandHandler


@dataclass(frozen=True, slots=True)
class InputDTO:

    user_id: UUID
    username: str
    created_at: datetime


class EnsureUser(CommandHandler):

    def __init__(
        self,
        user_repo: repositories.UserRepository,
        uow: UnitOfWork
    ) -> None:
        self.user_repo = user_repo
        self.uow = uow
    
    async def __call__(self, data: InputDTO) -> None:
        # 1.Ensure user doesn't exist
        if await self.user_repo.check_user_exists(username=data.username):
            raise user_exceptions.UserAlreadyExistsError()

        # 2.Create `User`
        user = User.create(
            user_id=data.user_id, username=data.username,
            created_at=data.created_at
        )
        await self.user_repo.save_user(user)

        await self.uow.commit()