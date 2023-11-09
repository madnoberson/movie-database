from uuid import UUID
from asyncpg.connection import Connection

from app.domain.models.achievement import Achievement, AchievementTypeEnum
from app.application.common.interfaces.repositories import AchievementRepository


class AchievementRepositoryImpl(AchievementRepository):

    def __init__(self, connection: Connection) -> None:
        self.connection = connection
    
    async def check_achievement_exists(
        self, user_id: UUID, achievement_type: AchievementTypeEnum
    ) -> bool:
        data = await self.connection.fetchval(
            """
            SELECT 1 FROM user_achievements ua
            WHERE ua.user_id = $1 AND ua.type= $2
            """,
            user_id, achievement_type.value
        )
        return bool(data)
    
    async def save_achievement(self, achievement: Achievement) -> None:
        await self.connection.execute(
            """
            INSERT INTO user_achievements (user_id, type, created_at)
            VALUES ($1, $2, $3)
            """,
            achievement.user_id, achievement.type.value,
            achievement.created_at
        )