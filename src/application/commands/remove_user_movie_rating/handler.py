from dataclasses import dataclass

from src.application.common.result import Result
from src.application.common.errors.user import (
    UserDoesNotExistError
)
from src.application.common.errors.movie import (
    MovieDoesNotExistError
)
from src.application.common.errors.user_movie_rating import (
    UserMovieRatingDoesNotExistError
)
from src.domain.models.user.value_objects import UserId
from src.domain.models.movie.value_objects import MovieId
from .command import (
    RemoveUserMovieRatingCommand,
    RemoveUserMovieRatingCommandResult
)
from .interfaces import RemoveUserMovieRatingCommandDBGateway


CommandHandlerResult = (
    Result[RemoveUserMovieRatingCommandResult, None] |
    Result[None, UserDoesNotExistError] |
    Result[None, MovieDoesNotExistError] |
    Result[None, UserMovieRatingDoesNotExistError]
)


@dataclass(frozen=True, slots=True)
class RemoveUserMovieRatingCommandHandler:

    db_gateway: RemoveUserMovieRatingCommandDBGateway

    def __call__(
        self,
        command: RemoveUserMovieRatingCommand
    ) -> CommandHandlerResult:
        user_id = UserId(command.user_id)
        user_exists = self.db_gateway.check_user_id_existence(
            user_id=user_id
        )
        if not user_exists:
            error = UserDoesNotExistError(user_id.value)
            return Result(value=None, error=error)

        movie_id = MovieId(command.movie_id)
        movie = self.db_gateway.get_movie_by_id(
            movie_id=movie_id
        )
        if movie is None:
            error = MovieDoesNotExistError(movie_id.value)
            return Result(value=None, error=error)
        
        umr = self.db_gateway.get_user_movie_rating_by_user_id_and_movie_id(
            user_id=user_id,
            movie_id=movie_id
        )
        if umr is None:
            error = UserMovieRatingDoesNotExistError(movie_id.value)
            return Result(value=None, error=error)
        
        movie.remove_rating(umr.rating)        
        self.db_gateway.update_movie(movie)
        self.db_gateway.remove_user_movie_rating_by_user_id_and_movie_id(
            user_id=user_id,
            movie_id=movie_id
        )
        self.db_gateway.commit()

        command_result = RemoveUserMovieRatingCommandResult(
            new_movie_rating=movie.rating,
            new_movie_rating_count=movie.rating_count
        )
        result = Result(value=command_result, error=None)

        return result