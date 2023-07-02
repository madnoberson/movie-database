from __future__ import annotations
from dataclasses import dataclass

from src.domain.models.movie.value_objects import MovieId
from .constants import MovieGenreEnum


@dataclass(slots=True)
class MovieGenres:

    movie_id: MovieId
    genres: list[MovieGenreEnum]

    @classmethod
    def create(
        cls,
        movie_id: MovieId,
        genres: list[MovieGenreEnum]
    ) -> MovieGenres:
        return MovieGenres(
            movie_id=movie_id,
            genres=genres
        )
