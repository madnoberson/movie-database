from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from .model import Model


@dataclass(slots=True)
class Movie(Model):

    id: UUID
    en_name: str
    created_at: datetime

    @classmethod
    def create(
        cls, movie_id: UUID, en_name: str,
        created_at: datetime
    ) -> "Movie":
        return Movie(
            id=movie_id, en_name=en_name,
            created_at=created_at
        )