from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from .model import Model


@dataclass(slots=True)
class DelayedMovie(Model):

    user_id: UUID
    movie_id: UUID
    created_at: datetime

    @classmethod
    def create(
        cls, user_id: UUID, movie_id: UUID,
        created_at: datetime
    ) -> "DelayedMovie":
        return DelayedMovie(
            user_id=user_id, movie_id=movie_id,
            created_at=created_at
        )
