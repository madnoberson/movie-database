from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.models.achievement import Achievement, AchievementTypeEnum


class AchievementRepository(ABC):

    @abstractmethod
    async def check_achievement_exists(
        self, user_id: UUID, achievement_type: AchievementTypeEnum
    ) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def save_achievement(self, achievement: Achievement) -> None:
        raise NotImplementedError