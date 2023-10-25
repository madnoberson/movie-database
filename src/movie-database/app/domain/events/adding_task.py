from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from app.domain.models.adding_task import AddingTaskTypeEnum
from .event import Event


class AddingTaskEvent(Event):
    ...


@dataclass(frozen=True, slots=True)
class AddingTaskCreatedEvent(AddingTaskEvent):
    
    id: UUID
    creator_id: UUID
    adding_type: AddingTaskTypeEnum
    kinopoisk_id: str
    created_at: datetime