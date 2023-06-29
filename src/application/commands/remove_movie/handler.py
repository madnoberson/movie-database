from dataclasses import dataclass

from src.application.common.result import Result
from src.application.common.errors.movie import MovieDoesNotExistError
from src.domain.models.movie.value_objects import MovieId
from .command import RemoveMovieCommand
from .interfaces import RemoveMovieCommandDBGateway


CommandHandlerResult = (
    Result[None, None] |
    Result[None, MovieDoesNotExistError]
)


@dataclass(frozen=True, slots=True)
class RemoveMovieCommandHandler:

    db_gateway: RemoveMovieCommandDBGateway

    def __call__(self, command: RemoveMovieCommand) -> CommandHandlerResult:
        movie_id = MovieId(command.movie_id)

        movie_exists = self.db_gateway.check_movie_existence_by_id(
            movie_id=movie_id
        )
        if not movie_exists:
            error = MovieDoesNotExistError(movie_id.value)
            return Result(value=None, error=error)
        
        self.db_gateway.remove_movie_by_id(movie_id.value)
        self.db_gateway.commit()

        return Result(value=None, error=None)
