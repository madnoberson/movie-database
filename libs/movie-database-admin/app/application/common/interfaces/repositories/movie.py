from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.models.movie import Movie


class MovieRepository(ABC):

    @abstractmethod
    async def save_movie(self, movie: Movie) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_movie(self, movie_id: UUID) -> Movie | None:
        raise NotImplementedError
    
    @abstractmethod
    async def update_movie(self, movie: Movie) -> None:
        raise NotImplementedError