from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.models.movie_rating import MovieRating


class MovieRatingRepository(ABC):

    @abstractmethod
    async def check_movie_rating_exists(
        self, user_id: UUID, movie_id: UUID
    ) -> bool:
        raise NotImplementedError
    
    @abstractmethod
    async def save_movie_rating(
        self, movie_rating: MovieRating
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_movie_rating(
        self, user_id: UUID, movie_id: UUID
    ) -> MovieRating | None:
        raise NotImplementedError
    
    @abstractmethod
    async def update_movie_rating(
        self, movie_rating: MovieRating
    ) -> None:
        raise NotImplementedError
    
    @abstractmethod
    async def delete_movie_rating(
        self, user_id: UUID, movie_id: UUID
    ) -> None:
        raise NotImplementedError