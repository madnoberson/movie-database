from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from .model import Model


@dataclass(slots=True)
class EnrichmentTask(Model):

    id: UUID
    user_id: UUID
    kinopoisk_id: str
    created_at: datetime

    finished_at: datetime | None

    @classmethod
    def create(
        self, enrichment_task_id: UUID, user_id: UUID,
        kinopoisk_id: str, created_at: datetime
    ) -> "EnrichmentTask":
        return EnrichmentTask(
            id=enrichment_task_id, user_id=user_id,
            kinopoisk_id=kinopoisk_id, created_at=created_at,
            finished_at=None
        )
    
    @property
    def is_finished(self) -> bool:
        return self.finished_at is not None
    
    def finish(self, finished_at: datetime) -> None:
        self.finished_at = finished_at