from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from .event import Event


@dataclass(frozen=True, slots=True)
class MovieRated(Event):

    user_id: UUID
    movie_id: UUID
    rating: float
    created_at: datetime