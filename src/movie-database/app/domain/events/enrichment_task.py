from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from .event import Event


@dataclass(frozen=True, slots=True)
class EnrichmentTaskCreatedEvent(Event):
    
    id: UUID
    user_id: UUID
    kinopoisk_id: str
    created_at: datetime