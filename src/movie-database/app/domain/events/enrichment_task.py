from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from app.domain.models.enrichment_task import EnrichmentTaskTypeEnum
from .event import Event


@dataclass(frozen=True, slots=True)
class EnrichmentTaskCreatedEvent(Event):
    
    id: UUID
    user_id: UUID
    enrichment_type: EnrichmentTaskTypeEnum
    kinopoisk_id: str
    created_at: datetime