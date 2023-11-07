from dataclasses import dataclass
from datetime import datetime
from uuid import UUID, uuid4

from app.domain.models.movie import Movie
from app.domain.events.movie import MovieCreated
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
        # 1.Ensure current superuser can create movie
        access_policy = await self.identity_provider.get_access_policy()
        self.access_service.ensure_can_create_movie(access_policy)

        # 2.Create movie
        movie = Movie.create(
            movie_id=uuid4(), en_name=data.en_name,
            created_at=datetime.utcnow()
        )
        await self.movie_repo.save_movie(movie)

        # 3.Publish `MovieCreated` event to event bus
        movie_created_event = MovieCreated(
            movie_id=movie.id, en_name=movie.en_name,
            created_at=movie.created_at
        )
        await self.event_bus.publish(movie_created_event)

        await self.uow.commit()

        return OutputDTO(movie_id=movie.id)