from abc import abstractmethod
from typing import Protocol

from src.domain.models.movie.model import Movie
from src.domain.models.movie.value_objects import MovieId


class SupportsGetMovieById(Protocol):

    @abstractmethod
    def get_movie_by_id(self, movie_id: MovieId) -> Movie | None:
        raise NotImplementedError


class SupportsSaveMovie(Protocol):

    @abstractmethod
    def save_movie(self, movie: Movie) -> None:
        raise NotImplementedError
    