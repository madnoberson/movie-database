from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from .event import Event


@dataclass(frozen=True, slots=True)
class MovieRated(Event):

    user_id: UUID
    movie_id: UUID
    rating: float
    is_full: bool
    created_at: datetime


@dataclass(frozen=True, slots=True)
class MovieRerated(Event):

    user_id: UUID
    movie_id: UUID
    rating: float
    is_full: bool
    updated_at: datetime
    