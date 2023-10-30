from dataclasses import dataclass
from datetime import datetime
from uuid import UUID, uuid4

from app.domain.models.user import User
from app.domain.events.user import UserCreated
from app.application.common.interfaces.event_bus import EventBus
from app.application.common.interfaces.uow import UnitOfWork
from app.application.common.interfaces import repositories
from app.application.common.exceptions import user as user_exceptions
from app.application.commands.handler import CommandHandler


@dataclass(frozen=True, slots=True)
class InputDTO:

    username: str
    password: str


@dataclass(frozen=True, slots=True)
class OutputDTO:

    user_id: UUID


class Register(CommandHandler):

    def __init__(
        self,
        user_repo: repositories.UserRepository,
        event_bus: EventBus,
        uow: UnitOfWork
    ) -> None:
        self.user_repo = user_repo
        self.event_bus = event_bus
        self.uow = uow

    async def __call__(self, data: InputDTO) -> OutputDTO:
        # 1.Ensure user doesn't exist
        user_exists = await self.user_repo.check_user_exists(username=data.username)
        if user_exists:
            raise user_exceptions.UserAlreadyExistsError()
        
        # 2.Create `User`
        user = User.create(
            user_id=uuid4(), username=data.username,
            password=data.password, created_at=datetime.utcnow()
        )
        await self.user_repo.save_user(user)

        # 3.Publish `UserCreated` event
        user_created_event = UserCreated(
            user_id=user.id, username=user.username,
            created_at=user.created_at
        )
        await self.event_bus.publish(user_created_event)

        await self.uow.commit()

        return OutputDTO(user_id=user.id)
