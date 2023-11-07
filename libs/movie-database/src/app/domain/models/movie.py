from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from .model import Model


@dataclass(slots=True)
class Movie(Model):

    id: UUID
    en_name: str
    created_at: datetime
    user_rating_count: int

    user_rating: float | None

    @classmethod
    def create(
        cls, movie_id: UUID, en_name: str,
        created_at: datetime
    ) -> "Movie":
        return Movie(
            id=movie_id, en_name=en_name,
            created_at=created_at, user_rating=None
        )

    def add_user_rating(self, user_rating: float) -> None:
        if self.user_rating_count == 0:
            self.user_rating = user_rating
            self.user_rating_count = 1
            return
        new_user_rating = (
            (self.user_rating * self.user_rating_count) + 
            user_rating
        )
        self.user_rating = (
            new_user_rating / (self.user_rating_count + 1)
        )
        self.user_rating_count += 1
    
    def remove_user_rating(self, user_rating: float) -> None:
        if self.user_rating_count == 1:
            self.user_rating = None
            self.user_rating_count = 0
            return
        new_user_rating = (
            (self.user_rating * self.user_rating_count) -
            user_rating
        )
        self.user_rating = (
            new_user_rating / (self.user_rating_count - 1)
        )
        self.user_rating_count -= 1