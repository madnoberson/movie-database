from dataclasses import dataclass
from uuid import uuid4

from src.application.common.result import Result
from src.domain.models.movie.model import Movie
from src.domain.models.movie.value_objects import (
    MovieId,
    MovieTitle
)
from .command import AddMovieCommand, AddMovieCommandResult
from .interfaces import AddMovieCommandDBGateway


CommandHandlerResult = (
    Result[AddMovieCommandResult, None]
)


@dataclass(frozen=True, slots=True)
class AddMovieCommandHandler:

    db_gateway: AddMovieCommandDBGateway

    def __call__(
        self,
        command: AddMovieCommand
    ) -> CommandHandlerResult:
        movie = Movie.create(
            id=MovieId(uuid4()),
            title=MovieTitle(command.title),
            release_date=command.release_date
        )

        self.db_gateway.save_movie(movie)
        self.db_gateway.commit()

        command_result = AddMovieCommandResult(movie.id.value)
        result = Result(value=command_result, error=None)

        return result