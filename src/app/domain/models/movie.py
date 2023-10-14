from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from app.domain.common.model import Model


@dataclass(slots=True)
class Movie(Model):

    id: UUID
    title: str
    created_at: datetime

    @classmethod
    def create(cls, movie_id: UUID, title: str, created_at: datetime) -> "Movie":
        return Movie(id=movie_id, title=title, created_at=created_at)