from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from .event import Event


@dataclass(frozen=True, slots=True)
class MovieCreated(Event):

    movie_id: UUID
    en_name: str
    created_at: datetime