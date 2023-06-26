from datetime import date
from uuid import UUID

import pytest

from src.application.commands.add_movie.command import (
    AddMovieCommand,
    AddMovieCommandResult
)
from src.application.commands.add_movie.handler import (
    AddMovieCommandHandler
)
from src.application.commands.add_movie.interfaces import (
    AddMovieCommandDBGateway
)
from src.domain.models.movie.model import Movie


class AddMovieCommandDBGatewayMock(
    AddMovieCommandDBGateway
):

    def save_movie(self, movie: Movie) -> None:
        ...
    
    def commit(self) -> None:
        ...
    
    def rollback(self) -> None:
        ...


class TestAddMovieCommand:

    def test_valid_args(self):
        try:
            AddMovieCommand(
                title="1917",
                release_date=date(2019, 1, 30)
            )
        except ValueError:
            pytest.fail()
    
    def test_invalid_args(self):
        with pytest.raises(ValueError):
            AddMovieCommand(
                title="",
                release_date="01.01.2001"
            )
            AddMovieCommand(
                title=1917,
                release_date=date(2019, 1, 30)
            )


class TestAddMovieCommandHandler:
    
    def test_handler_should_return_movie_id(self):
        handler = AddMovieCommandHandler(
            db_gateway=AddMovieCommandDBGatewayMock()
        )

        command = AddMovieCommand(
            title="There will be blood",
            release_date=date(2008, 2, 28)
        )
        result = handler(command)

        assert result.error == None
        assert isinstance(result.value, AddMovieCommandResult)
        assert isinstance(result.value.movie_id, UUID)