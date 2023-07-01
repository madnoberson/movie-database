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


class SupportsUpdateMovie(Protocol):

    @abstractmethod
    def update_movie(self, movie: Movie) -> None:
        raise NotImplementedError


class SupportsCheckMovieIdExistence(Protocol):

    @abstractmethod
    def check_movie_existence_by_id(self, movie_id: MovieId) -> bool:
        raise NotImplementedError


class SupportsRemoveMovie(Protocol):

    @abstractmethod
    def remove_movie_by_id(self, movie_id: MovieId) -> None:
        raise NotImplementedError
    