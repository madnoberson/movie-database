from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from .model import Model


@dataclass(slots=True)
class MovieRating(Model):

    user_id: UUID
    movie_id: UUID
    rating: float
    is_full: bool
    created_at: datetime

    updated_at: datetime | None

    @classmethod
    def create(
        cls, user_id: UUID, movie_id: UUID,
        rating: float, created_at: datetime,
        is_full: bool = False
    ) -> "MovieRating":
        return MovieRating(
            user_id=user_id, movie_id=movie_id,
            rating=rating, is_full=is_full,
            created_at=created_at, updated_at=None
        )

    def update(self, rating: float, updated_at: datetime) -> None:
        self.rating = rating
        self.updated_at = updated_at
    
    def make_full(self) -> None:
        self.is_full = True