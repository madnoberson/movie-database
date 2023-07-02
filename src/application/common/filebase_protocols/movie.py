from abc import abstractmethod
from typing import Protocol

from src.domain.models.movie.value_objects import MoviePosterKey


class SupportsSaveMoviePoster(Protocol):

    @abstractmethod
    def save_movie_poster(
        self,
        poster: bytes,
        key: MoviePosterKey
    ) -> None:
        raise NotImplementedError