from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from .model import Model


@dataclass(slots=True)
class MovieRating(Model):

    id: UUID
    user_id: UUID
    movie_id: UUID
    rating: float
    created_at: datetime

    updated_at: datetime | None

    @classmethod
    def create(
        cls, movie_rating_id: UUID, user_id: UUID,
        movie_id: UUID, created_at: datetime,
        rating: float
    ) -> "MovieRating":
        return MovieRating(
            id=movie_rating_id, user_id=user_id,
            movie_id=movie_id, created_at=created_at,
            rating=rating
        )

    def update(self, rating: float, updated_at: datetime) -> None:
        self.rating = rating
        self.updated_at = updated_at