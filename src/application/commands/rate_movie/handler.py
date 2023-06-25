from dataclasses import dataclass
from datetime import datetime

from src.application.common.result import Result
from src.application.common.errors.user import (
    UserDoesNotExist
)
from src.application.common.errors.movie import (
    MovieDoesNotExist
)
from src.domain.models.user_movie_rating.model import (
    UserMovieRating
)
from src.domain.models.user.value_objects import UserId
from src.domain.models.movie.value_objects import MovieId
from .command import (
    RateMovieCommand,
    RateMovieCommandResult
)
from .interfaces import RateMovieDBGateway
from .errors import UserMovieRatingAlreadyExists


CommandHandlerResult = (
    Result[RateMovieCommandResult, None],
    Result[None, UserDoesNotExist],
    Result[None, MovieDoesNotExist],
    Result[None, UserMovieRatingAlreadyExists],
)
    

@dataclass(frozen=True, slots=True)
class RateMovieCommandHandler:

    db_gateway: RateMovieDBGateway

    def __call__(
        self,
        command: RateMovieCommand
    ) -> CommandHandlerResult:
        user_id = UserId(command.user_id)
        user_exists = self.db_gateway.check_user_id_existence(
            user_id=user_id
        )
        if not user_exists:
            error = UserDoesNotExist(user_id.value)
            return Result(value=None, error=error)
        
        movie_id = MovieId(command.movie_id)
        movie = self.db_gateway.get_movie_by_id(
            movie_id=movie_id
        )
        if movie is None:
            error = MovieDoesNotExist(movie_id.value)
            return Result(value=None, error=error)

        umr_exists = self.db_gateway.check_user_movie_rating_existence(
            user_id=user_id,
            movie_id=movie_id
        )
        if umr_exists:
            error = UserMovieRatingAlreadyExists(movie_id.value)
            return Result(value=None, error=error)
        
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

        command_result = RateMovieCommandResult(
            new_movie_rating=movie.rating,
            user_rating=command.rating,
            user_rating_created_at=user_movie_rating.created_at
        )
        result = Result(value=command_result, error=None)

        return result