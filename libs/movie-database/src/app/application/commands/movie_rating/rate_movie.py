from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from app.domain.models.user import User
from app.domain.models.movie_rating import MovieRating
from app.domain.models.achievement import Achievement
from app.domain.events.movie_rating import MovieRated
from app.domain.events.achievement import AchievementObtained
from app.domain.services.movie_rating import MovieRatingService
from app.domain.services.achievement import AchievementService
from app.application.common.interfaces.identity_provider import IdentityProvider
from app.application.common.interfaces.event_bus import EventBus
from app.application.common.interfaces.uow import UnitOfWork
from app.application.common.interfaces import repositories
from app.application.common.exceptions import movie as movie_exceptions
from app.application.common.exceptions import movie_rating as movie_rating_exceptions
from app.application.commands.handler import CommandHandler


@dataclass(frozen=True, slots=True)
class InputDTO:

    movie_id: UUID
    rating: float


class RateMovie(CommandHandler):

    def __init__(
        self,
        movie_rating_repo: repositories.MovieRatingRepository,
        movie_repo: repositories.MovieRepository,
        user_repo: repositories.UserRepository,
        achievement_repo: repositories.AchievementRepository,
        movies_rating_policy_repo: repositories.MoviesRatingPolicyRepository,
        rated_movies_achievements_policy_repo: repositories.RatedMoviesAchievementsPolicyRepository,
        event_bus: EventBus,
        identity_provider: IdentityProvider,
        movie_rating_service: MovieRatingService,
        achievement_service: AchievementService,
        uow: UnitOfWork
    ) -> None:
        self.movie_rating_repo = movie_rating_repo
        self.movie_repo = movie_repo
        self.user_repo = user_repo
        self.achievement_repo = achievement_repo
        self.movies_rating_policy_repo = movies_rating_policy_repo
        self.rated_movies_achievements_policy_repo = rated_movies_achievements_policy_repo
        self.event_bus = event_bus
        self.identity_provider = identity_provider
        self.movie_rating_service = movie_rating_service
        self.achievement_service = achievement_service
        self.uow = uow
    
    async def __call__(self, data: InputDTO) -> None:
        current_user_id = await self.identity_provider.get_current_user_id()
        current_user = await self.user_repo.get_user(user_id=current_user_id)

        await self._rate_movie(
            current_user=current_user, movie_id=data.movie_id,
            rating=data.rating
        )
        await self._give_achievements(current_user=current_user)

        await self.uow.commit()
    
    async def _rate_movie(self, current_user: User, movie_id: UUID, rating: float) -> None:
        # 1.Ensure movie is not rated by user
        if await self.movie_rating_repo.check_movie_rating_exists(
            user_id=current_user.id, movie_id=movie_id
        ):
            raise movie_rating_exceptions.MovieRatingAlreadyExistsError()
        
        # 2.Ensure movie exists
        movie = await self.movie_repo.get_movie(movie_id=movie_id)
        if movie is None:
            raise movie_exceptions.MovieDoesNotExistError()

        # 3.Get movies rating policy
        movies_rating_policy = (
            await self.movies_rating_policy_repo.get_movies_rating_policy()
        )

        # 4.Update movie's rating if movie rating is 'full'
        movie_rating_is_full = (
            self.movie_rating_service.check_user_can_fully_rate_movie(
                user=current_user, movies_rating_policy=movies_rating_policy
            )
        )
        if movie_rating_is_full:
            movie.add_user_rating(user_rating=rating)
            await self.movie_repo.update_movie(movie)

        # 5.Create movie rating
        movie_rating = MovieRating.create(
            user_id=current_user.id, movie_id=movie.id, rating=rating,
            created_at=datetime.utcnow(), is_full=movie_rating_is_full
        )
        await self.movie_rating_repo.save_movie_rating(movie_rating)

        # 6.Update user rated movies count
        current_user.add_movie_rating()
        await self.user_repo.update_user(current_user)

        # 7.Publish `MovieRated` event to event bus
        movie_rated_event = MovieRated(
            user_id=movie_rating.user_id, movie_id=movie_rating.movie_id,
            rating=movie_rating.rating, is_full=movie_rating.is_full,
            created_at=movie_rating.created_at
        )
        await self.event_bus.publish(movie_rated_event)
    
    async def _give_achievements(self, current_user: User) -> None:
        # 1.Get rated movies achievements policy
        rated_movies_achievements_policy = (
            await self.rated_movies_achievements_policy_repo.
            get_rated_movies_achievements_policy()
        )

        # 2.Create achievement and publish `AchievementObtained` event to event bus
        # if user can obtain rated movies achievement and achievement doesn't exist
        achievement_type = self.achievement_service.get_rated_movie_achievement_type(
            user=current_user,
            rated_movies_achievements_policy=rated_movies_achievements_policy
        )
        if (
            achievement_type is not None and
            await self.achievement_repo.check_achievement_exists(
                user_id=current_user.id, achievement_type=achievement_type
            )
        ):
            # 2.1.Create achievement
            achievement = Achievement.create(
                user_id=current_user.id, type=achievement_type,
                created_at=datetime.utcnow()
            )
            await self.achievement_repo.save_achievement(achievement)

            # 2.2.Publish `AchievementObtained` event to event bus
            achievement_obtained_event = AchievementObtained(
                user_id=current_user.id, type=achievement_type,
                created_at=achievement.created_at
            )
            await self.event_bus.publish(achievement_obtained_event)