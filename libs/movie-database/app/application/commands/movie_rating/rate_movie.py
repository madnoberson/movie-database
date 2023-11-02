from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from app.domain.models.movie_rating import MovieRating
from app.domain.events.movie_rating import MovieRated
from app.application.common.interfaces.identity_provider import IdentityProvider
from app.application.common.interfaces.event_bus import EventBus
from app.application.common.interfaces.uow import UnitOfWork
from app.application.common.interfaces import repositories
from app.application.common.exceptions import movie as movie_exceptions
from app.application.common.exceptions import movie_rating as movie_rating_exceptions
from app.application.commands.handler import CommandHandler


@dataclass(frozen=True, slots=True)
class InputDTO:

    user_id: UUID
    movie_id: UUID
    rating: float


class RateMovie(CommandHandler):

    def __init__(
        self,
        movie_rating_repo: repositories.MovieRatingRepository,
        movie_repo: repositories.MovieRepository,
        event_bus: EventBus,
        identity_provider: IdentityProvider,
        uow: UnitOfWork
    ) -> None:
        self.movie_rating_repo = movie_rating_repo
        self.movie_repo = movie_repo
        self.event_bus = event_bus
        self.identity_provider = identity_provider
        self.uow = uow
    
    async def __call__(self, data: InputDTO) -> None:
        # 1.Get current user id
        current_user_id = await self.identity_provider.get_current_user_id()

        # 2.Ensure movie is not rated by user
        if await self.movie_rating_repo.check_movie_rating_exists(
            user_id=current_user_id, movie_id=data.movie_id
        ):
            raise movie_rating_exceptions.MovieRatingAlreadyExistsError()
        
        # 3.Get movie
        movie = await self.movie_repo.get_movie(movie_id=data.movie_id)
        if movie is None:
            raise movie_exceptions.MovieDoesNotExistError()
        
        # 4.Create movie rating
        movie_rating = MovieRating.create(
            user_id=current_user_id, movie_id=movie.id,
            rating=data.rating, created_at=datetime.utcnow()
        )
        await self.movie_rating_repo.save_movie_rating(movie_rating)

        # 5.Update movie user rating
        movie.add_user_rating(user_rating=data.rating)
        await self.movie_repo.save_movie(movie)

        # 6.Publish `MovieRated` event to event bus
        movie_rated_event = MovieRated(
            user_id=movie_rating.user_id, movie_id=movie_rating.movie_id,
            rating=movie_rating.rating, created_at=movie_rating.created_at
        )
        await self.event_bus.publish(movie_rated_event)

        await self.uow.commit()