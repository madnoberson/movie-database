from abc import abstractmethod
from typing import Protocol

from src.domain.models.movie_genres.model import MovieGenres


class SupportsSaveMovieGenres(Protocol):

    @abstractmethod
    def save_movie_genres(
        self,
        movie_genres: MovieGenres
    ) -> None:
        raise NotImplementedError