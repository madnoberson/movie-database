from dataclasses import dataclass
from uuid import uuid4

from src.domain.models.movie.model import Movie
from src.domain.models.movie.value_objects import (
    MovieId,
    MovieTitle,
    MoviePosterKey
)
from .command import AddMovieCommand, AddMovieCommandResult
from .interfaces import AddMovieCommandDBGateway, AddMovieCommandFBGateway


@dataclass(frozen=True, slots=True)
class AddMovieCommandHandler:
    """
    Returns:
        * `AddMovieCommandResult`
    """

    db_gateway: AddMovieCommandDBGateway
    fb_gateway: AddMovieCommandFBGateway

    def __call__(
        self,
        command: AddMovieCommand
    ) -> AddMovieCommandResult:
        movie_uuid = uuid4()

        if movie_poster_key := command.poster:
            movie_poster_key = MoviePosterKey(
                value=f"{movie_uuid}-poster.png"
            )
            self.fb_gateway.save_movie_poster(
                poster=command.poster,
                key=movie_poster_key
            )

        movie = Movie.create(
            id=MovieId(movie_uuid),
            title=MovieTitle(command.title),
            release_date=command.release_date,
            status=command.status,
            genres=command.genres,
            mpaa=command.mpaa,
            poster_key=movie_poster_key
        )

        self.db_gateway.save_movie(movie)
        self.db_gateway.commit()

        return AddMovieCommandResult(movie.id.value)
        