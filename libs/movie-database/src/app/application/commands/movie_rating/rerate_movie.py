from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from app.domain.events.movie_rating import MovieRerated
from app.domain.services.movie_rating import MovieRatingService
from app.application.common.interfaces.identity_provider import IdentityProvider
from app.application.common.interfaces.event_bus import EventBus
from app.application.common.interfaces.uow import UnitOfWork
from app.application.common.interfaces import repositories
from app.application.common.exceptions import movie_rating as movie_rating_exceptions
from app.application.commands.handler import CommandHandler


@dataclass(frozen=True, slots=True)
class InputDTO:

    movie_id: UUID
    rating: float


class RerateMovie(CommandHandler):

    def __init__(
        self,
        movie_rating_repo: repositories.MovieRatingRepository,
        movie_repo: repositories.MovieRepository,
        user_repo: repositories.UserRepository,
        movies_rating_policy_repo: repositories.MoviesRatingPolicyRepository,
        event_bus: EventBus,
        identity_provider: IdentityProvider,
        movie_rating_service: MovieRatingService,
        uow: UnitOfWork   
    ) -> None:
        self.movie_rating_repo = movie_rating_repo
        self.movie_repo = movie_repo
        self.user_repo = user_repo
        self.movies_rating_policy_repo = movies_rating_policy_repo
        self.event_bus = event_bus
        self.identity_provider = identity_provider
        self.movie_rating_service = movie_rating_service
        self.uow = uow
    
    async def __call__(self, data: InputDTO) -> None:
        # 1.Get current user id
        current_user_id = await self.identity_provider.get_current_user_id()

        # 2.Get movie rating
        movie_rating = await self.movie_rating_repo.get_movie_rating(
            user_id=current_user_id, movie_id=data.movie_id
        )
        if movie_rating is None:
            raise movie_rating_exceptions.MovieRatingDoesNotExistError()

        # 3.Update movie rating
        old_movie_rating = movie_rating.rating
        movie_rating.update(rating=data.rating, updated_at=datetime.utcnow())
        await self.movie_rating_repo.update_movie_rating(movie_rating)

        # 4.Get user
        user = await self.user_repo.get_user(user_id=current_user_id)

        # 5.Get movies rating policy
        movies_rating_policy = (
            await self.movies_rating_policy_repo.get_movies_rating_policy()
        )

        # 6.Update movie's rating if movie rating is full
        if self.movie_rating_service.check_user_can_fully_rerate_movie(
            user=user, movie_rating=movie_rating,
            movies_rating_policy=movies_rating_policy
        ):
            # 6.1.Get movie
            movie = await self.movie_repo.get_movie(movie_id=data.movie_id)

            # 6.2.Update movie's rating
            movie.remove_user_rating(user_rating=old_movie_rating)
            movie.add_user_rating(user_rating=data.rating)
            await self.movie_repo.update_movie(movie)

        # 7.Update user rated movies count
        user.add_movie_rating()
        await self.user_repo.update_user(user)

        # 8.Publish `MovieRerated` event to event bus
        movie_rated_event = MovieRerated(
            user_id=movie_rating.user_id, movie_id=movie_rating.movie_id,
            rating=movie_rating.rating, is_full=movie_rating.is_full,
            updated_at=movie_rating.updated_at
        )
        await self.event_bus.publish(movie_rated_event)

        await self.uow.commit()