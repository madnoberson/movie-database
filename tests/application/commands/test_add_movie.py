from dataclasses import dataclass
from datetime import date

import pytest

from src.application.commands.add_movie.command import (
    AddMovieCommand,
    AddMovieCommandResult
)
from src.application.commands.add_movie.handler import (
    AddMovieCommandHandler
)
from src.application.commands.add_movie.interfaces import (
    AddMovieCommandDBGateway,
    AddMovieCommandFBGateway
)
from src.domain.models.movie.model import Movie
from src.domain.models.movie.value_objects import MoviePosterKey
from src.domain.models.movie.constants import (
    MovieStatusEnum,
    MPAAEnum
)
from src.domain.models.movie_genres.constants import MovieGenreEnum
from src.domain.models.movie_genres.model import MovieGenres


@dataclass(slots=True)
class AddMovieCommandDBGatewaySpy(
    AddMovieCommandDBGateway
):
    
    movie_added: bool = False
    movie_genres_added: bool = False

    def save_movie(self, movie: Movie) -> None:
        self.movie_added = True
    
    def save_movie_genres(
        self,
        movie_genres: MovieGenres
    ) -> None:
        self.movie_genres_added = True
    
    def commit(self) -> None:
        ...
    
    def rollback(self) -> None:
        ...


@dataclass(slots=True)
class AddMovieCommandFBGatewaySpy(
    AddMovieCommandFBGateway
):

    poster_added: bool = False

    def save_movie_poster(
        self,
        poster: bytes,
        key: MoviePosterKey
    ) -> None:
        self.poster_added = True


class TestAddMovieCommand:

    def test_valid_args(self):
        try:
            AddMovieCommand(
                title="1917",
                release_date=date(2019, 1, 30),
                status=MovieStatusEnum(0),
                genres=[MovieGenreEnum(0), MovieGenreEnum(1)],
                mpaa=MPAAEnum(0),
                poster=bytes("postery_bytes", encoding="utf-8")
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
            AddMovieCommand(
                title="",
                release_date="01.01.2001",
                poster="file.jpg"
            )


class TestAddMovieCommandHandler:
    
    def test_handler_should_return_movie_id(self):
        db_gateway=AddMovieCommandDBGatewaySpy()
        fb_gateway=AddMovieCommandFBGatewaySpy()

        handler = AddMovieCommandHandler(
            db_gateway=db_gateway,
            fb_gateway=fb_gateway
        )

        command = AddMovieCommand(
            title="There will be blood",
            release_date=date(2008, 2, 28),
            poster=bytes("poster_bytes", encoding="utf-8"),
            status=MovieStatusEnum(0),
            genres=[MovieGenreEnum(1), MovieGenreEnum(6)],
            mpaa=MPAAEnum(3)
        )
        result = handler(command)

        assert result.error == None
        assert isinstance(result.value, AddMovieCommandResult)
        assert db_gateway.movie_added
        assert db_gateway.movie_genres_added
        assert fb_gateway.poster_added