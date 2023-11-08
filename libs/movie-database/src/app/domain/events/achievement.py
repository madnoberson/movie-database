from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from app.domain.models.achievement import AchievementTypeEnum
from .event import Event


@dataclass(frozen=True, slots=True)
class AchievementObtained(Event):

    user_id: UUID
    type: AchievementTypeEnum
    created_at: datetime

