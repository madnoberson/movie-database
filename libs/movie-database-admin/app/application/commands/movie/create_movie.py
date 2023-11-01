from dataclasses import dataclass
from datetime import datetime
from uuid import UUID, uuid4

from app.domain.services.access import AccessService
from app.application.common.interfaces.identity_provider import IdentityProvider
from app.application.common.interfaces.event_bus import EventBus
from app.application.common.interfaces.uow import UnitOfWork
from app.application.common.interfaces import repositories
from app.application.commands.handler import CommandHandler


@dataclass(frozen=True, slots=True)
class InputDTO:

    en_name: str


@dataclass(frozen=True, slots=True)
class OutputDTO:

    movie_id: UUID


class CreateMovie(CommandHandler):

    def __init__(
        self,
        movie_repo: repositories.MovieRepository,
        event_bus: EventBus,
        identity_provider: IdentityProvider,
        access_service: AccessService,
        uow: UnitOfWork
    ) -> None:
        self.movie_repo = movie_repo
        self.event_bus = event_bus
        self.identity_provider = identity_provider
        self.access_service = access_service
        self.uow = uow
    
    async def __call__(self, data: InputDTO) -> None:
        ...