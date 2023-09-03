from abc import abstractmethod
from typing import Protocol
from uuid import UUID

from src.domain.movie import Movie


class SupportsSaveMovie(Protocol):

    @abstractmethod
    async def save_movie(self, movie: Movie) -> None:
        raise NotImplementedError


class SupportsGetMovie(Protocol):

    @abstractmethod
    async def get_movie(self, movie_id: UUID) -> Movie | None:
        raise NotImplementedError


class SupportsUpdateMovie(Protocol):

    @abstractmethod
    async def update_movie(self, movie: Movie) -> None:
        raise NotImplementedError