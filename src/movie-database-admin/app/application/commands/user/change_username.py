from dataclasses import dataclass

from app.domain.events.user import UsernameChanged
from app.domain.services.access import AccessService
from app.application.common.interfaces.identity_provider import IdentityProvider
from app.application.common.interfaces.event_bus import EventBus
from app.application.common.interfaces.uow import UnitOfWork
from app.application.common.interfaces import repositories
from app.application.common.exceptions import user as user_exceptions
from app.application.commands.handler import CommandHandler


@dataclass(frozen=True, slots=True)
class InputDTO:

    username: str


class ChangeUsername(CommandHandler):

    def __init__(
        self,
        user_repo: repositories.UserRepository,
        event_bus: EventBus,
        access_service: AccessService,
        identity_provider: IdentityProvider,
        uow: UnitOfWork
    ) -> None:
        self.user_repo = user_repo
        self.event_bus = event_bus
        self.access_service = access_service
        self.identity_provider = identity_provider
        self.uow = uow
    
    async def __call__(self, data: InputDTO) -> None:
        # 1.Ensure superuser can change username
        access_policy = await self.identity_provider.get_access_policy()
        self.access_service.ensure_can_change_username(access_policy)
        
        # 2.Get user and change username
        user = await self.user_repo.get_user(user_id=access_policy.superuser_id)
        if user is None:
            raise user_exceptions.UserDoesNotExistError()
        
        user.change_username(username=data.username)
        await self.user_repo.update_user(user)

        # 3.Publish `UsernameChanged` to event bus
        username_changed_event = UsernameChanged(
            user_id=access_policy.superuser_id, new_username=user.username
        )
        await self.event_bus.publish(username_changed_event)

        await self.uow.commit()