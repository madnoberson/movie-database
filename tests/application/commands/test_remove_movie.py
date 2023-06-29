from dataclasses import dataclass, field
from datetime import date
from uuid import uuid4

import pytest

from src.application.common.result import Result
from src.application.common.errors.movie import (
    MovieDoesNotExistError
)
from src.domain.models.movie.model import Movie
from src.domain.models.movie.value_objects import (
    MovieId, MovieTitle
)
from src.application.commands.remove_movie.command import (
    RemoveMovieCommand
)
from src.application.commands.remove_movie.interfaces import (
    RemoveMovieCommandDBGateway
)
from src.application.commands.remove_movie.handler import (
    RemoveMovieCommandHandler
)


@dataclass(frozen=True, slots=True)
class FakeRemoveMovieCommandDBGateway(
    RemoveMovieCommandDBGateway
):
    
    movies: dict[MovieId, Movie] = field(
        default_factory=dict
    )

    def check_movie_existence_by_id(
        self,
        movie_id: MovieId
    ) -> bool:
        return not self.movies.get(movie_id) is None

    def remove_movie_by_id(
        self,
        movie_id: MovieId
    ) -> None:
        self.movies.pop(movie_id, None)

    def commit(self) -> None:
        ...
    
    def rollback(self) -> None:
        ...


class TestRemoveMovieCommand:

    def test_valid_args(self):
        try:
            RemoveMovieCommand(
                movie_id=uuid4()
            )
        except ValueError:
            pytest.fail()
    
    def test_invalid_args(self):
        with pytest.raises(ValueError):
            RemoveMovieCommand(
                movie_id=1
            )


class TestRemoveMovieCommandHandler:

    def test_handler_should_return_none(self):
        movie = Movie(
            id=MovieId(uuid4()),
            title=MovieTitle("There will be blood"),
            release_date=date(2008, 2, 28),
            rating=0,
            rating_count=0
        )
        movies = {movie.id: movie}

        db_gateway = FakeRemoveMovieCommandDBGateway(movies)
        handler = RemoveMovieCommandHandler(db_gateway)
        
        command = RemoveMovieCommand(movie_id=movie.id.value)
        result = handler(command)

        assert result == Result(None, None)
    
    def test_handler_should_return_error_when_movie_does_not_exist(self):
        db_gateway = FakeRemoveMovieCommandDBGateway()
        handler = RemoveMovieCommandHandler(db_gateway)
        
        command = RemoveMovieCommand(movie_id=uuid4())
        result = handler(command)

        assert result == Result(None, MovieDoesNotExistError(command.movie_id))