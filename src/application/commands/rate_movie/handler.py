from dataclasses import dataclass
from datetime import datetime

from src.application.common.errors.user import UserDoesNotExistError
from src.application.common.errors.movie import MovieDoesNotExistError
from src.domain.models.user_movie_rating.model import UserMovieRating
from src.domain.models.user.value_objects import UserId
from src.domain.models.movie.value_objects import MovieId
from .command import RateMovieCommand, RateMovieCommandResult
from .interfaces import RateMovieCommandDBGateway
from .errors import UserMovieRatingAlreadyExistsError


@dataclass(frozen=True, slots=True)
class RateMovieCommandHandler:
    """
    Raises:
        * `UserDoesNotExistError`
        * `MovieDoesNotExistError`
        * `UserMovieRatingAlreadyExistsError` \n
    Returns:
        * `RateMovieCommandResult`
    """

    db_gateway: RateMovieCommandDBGateway

    def __call__(self, command: RateMovieCommand) -> RateMovieCommandResult:
        user_id = UserId(command.user_id)
        user_exists = self.db_gateway.check_user_id_existence(
            user_id=user_id
        )
        if not user_exists:
            raise UserDoesNotExistError(user_id.value)
        
        movie_id = MovieId(command.movie_id)
        movie = self.db_gateway.get_movie_by_id(
            movie_id=movie_id
        )
        if movie is None:
            raise MovieDoesNotExistError(movie_id.value)

        umr_exists = self.db_gateway.check_user_movie_rating_existence(
            user_id=user_id,
            movie_id=movie_id
        )
        if umr_exists:
            raise UserMovieRatingAlreadyExistsError(movie_id.value)
        
        user_movie_rating = UserMovieRating.create(
            user_id=user_id,
            movie_id=movie_id,
            rating=command.rating,
            created_at=datetime.utcnow()
        )
        self.db_gateway.save_user_movie_rating(user_movie_rating)
        
        movie.add_rating(command.rating)
        self.db_gateway.update_movie(movie)

        self.db_gateway.commit()

        return RateMovieCommandResult(
            new_movie_rating=movie.rating,
            new_movie_rating_count=movie.rating_count,
            user_rating=command.rating,
            user_rating_created_at=user_movie_rating.created_at
        )
        