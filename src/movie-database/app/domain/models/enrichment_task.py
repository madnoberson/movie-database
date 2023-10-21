from dataclasses import dataclass
from datetime import datetime
from enum import IntEnum
from uuid import UUID

from .model import Model


class EnrichmentTaskTypeEnum(IntEnum):

    MOVIE = 0


@dataclass(slots=True)
class EnrichmentTask(Model):

    id: UUID
    user_id: UUID
    enrichment_type: EnrichmentTaskTypeEnum
    kinopoisk_id: str
    created_at: datetime

    movie_id: UUID | None
    finished_at: datetime | None

    @classmethod
    def create(
        self, enrichment_task_id: UUID, user_id: UUID,
        enrichment_type: EnrichmentTaskTypeEnum,
        kinopoisk_id: str, created_at: datetime
    ) -> "EnrichmentTask":
        return EnrichmentTask(
            id=enrichment_task_id, user_id=user_id,
            enrichment_type=enrichment_type, kinopoisk_id=kinopoisk_id,
            created_at=created_at, movie_id=None, finished_at=None
        )
    
    @property
    def is_finished(self) -> bool:
        return self.finished_at is not None
    
    def finish(self, movie_id: UUID, finished_at: datetime) -> None:
        self.movie_id = movie_id
        self.finished_at = finished_at