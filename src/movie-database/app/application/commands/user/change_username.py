from dataclasses import dataclass

from app.domain.events.user import UsernameChanged
from app.application.common.interfaces.identity_provider import IdentityProvider
from app.application.common.interfaces.event_bus import EventBus
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
        event_bus: EventBus,
        identity_provider: IdentityProvider,
        uow: UnitOfWork
    ) -> None:
        self.user_repo = user_repo
        self.event_bus = event_bus
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

        # 3.Publish `UsernameChanged` to event bus
        username_changed_event = UsernameChanged(
            user_id=current_user_id, new_username=user.username
        )
        await self.event_bus.publish(username_changed_event)

        await self.uow.commit()