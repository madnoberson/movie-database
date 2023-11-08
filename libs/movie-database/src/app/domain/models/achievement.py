from dataclasses import dataclass
from datetime import datetime
from enum import IntEnum
from uuid import UUID

from .model import Model


class AchievementTypeEnum(IntEnum):

    FILMOPHILE_1 = 0
    FILMOPHILE_2 = 1
    FILMOPHILE_3 = 2
    FILMPPHILE_4 = 3


@dataclass(slots=True)
class Achievement(Model):

    user_id: UUID
    type: AchievementTypeEnum
    created_at: datetime

    @classmethod
    def create(
        cls, user_id: UUID,
        type: AchievementTypeEnum,
        created_at: datetime
    ) -> "Achievement":
        return Achievement(
            user_id=user_id, type=type,
            created_at=created_at
        )