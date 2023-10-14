from abc import ABC, abstractmethod

from app.domain.models.movie import Movie


class MovieRepository(ABC):

    @abstractmethod
    async def save_movie(self, movie: Movie) -> None:
        raise NotImplementedError