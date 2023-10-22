from dataclasses import dataclass
from datetime import datetime
from enum import IntEnum
from uuid import UUID

from .model import Model


class AddingTaskTypeEnum(IntEnum):

    MOVIE = 0


@dataclass(slots=True)
class AddingTask(Model):

    id: UUID
    creator_id: UUID
    adding_type: AddingTaskTypeEnum
    kinopoisk_id: str
    created_at: datetime

    related_to: UUID | None
    finished_at: datetime | None

    @classmethod
    def create(
        cls, adding_task_id: UUID, creator_id: UUID,
        adding_type: AddingTaskTypeEnum,
        kinopoisk_id: str, created_at: datetime
    ) -> "AddingTask":
        return AddingTask(
            id=adding_task_id, creator_id=creator_id,
            adding_type=adding_type, kinopoisk_id=kinopoisk_id,
            created_at=created_at, related_to=None, finished_at=None
        )
    
    @property
    def is_finished(self) -> bool:
        return self.finished_at is not None
    
    def finish(self, related_to: UUID, finished_at: datetime) -> None:
        self.related_to = related_to
        self.finished_at = finished_at