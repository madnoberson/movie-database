from dataclasses import dataclass
from datetime import datetime
from uuid import UUID, uuid4

from app.domain.models.user import User
from app.application.common.handler import CommandHandler
from app.application.common.interfaces.uow import UnitOfWork
from app.application.common.exceptions import user as user_exceptions
from app.application.common.interfaces.repositories import UserRepository


@dataclass(frozen=True, slots=True)
class InputDTO:

    username: str
    password: str


@dataclass(frozen=True, slots=True)
class OutputDTO:

    user_id: UUID


class Register(CommandHandler):

    def __init__(self, user_repo: UserRepository, uow: UnitOfWork) -> None:
        self.user_repo = user_repo
        self.uow = uow

    async def __call__(self, data: InputDTO) -> OutputDTO:
        # 1.Ensure user does not exist
        user_exists = await self.user_repo.check_user_exists(username=data.username)
        if user_exists:
            raise user_exceptions.UserAlreadyExistsError()
        
        # 2.Create user
        user = User.create(
            user_id=uuid4(), username=data.username,
            password=data.password, created_at=datetime.utcnow()
        )

        # 3.Save user
        await self.user_repo.save_user(user)
        await self.uow.commit()

        return OutputDTO(user_id=user.id)
