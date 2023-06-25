from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime

from src.domain.models.user.value_objects import UserId
from src.domain.models.movie.value_objects import MovieId


@dataclass(slots=True)
class UserMovieRating:

    user_id: UserId
    movie_id: MovieId
    rating: float
    created_at: datetime
    updated_at: datetime | None

    @classmethod
    def create(
        cls,
        user_id: UserId,
        movie_id: MovieId,
        rating: float,
        created_at: datetime
    ) -> UserMovieRating:
        return UserMovieRating(
            user_id=user_id,
            movie_id=movie_id,
            rating=rating,
            created_at=created_at,
            updated_at=None
        )

    def update(
        self,
        rating: float,
        updated_at: datetime
    ) -> None:
        self.rating = rating
        self.updated_at = updated_at
