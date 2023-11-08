from asyncpg.connection import Connection

from app.domain.policies import FilmophileAchievementsPolicy
from app.application.common.interfaces.repositories import FilmophileAchievementsPolicyRepository
from app.infrastructure.database.mappers import as_domain_policy


class FilmophileAchievementsPolicyRepositoryImpl(FilmophileAchievementsPolicyRepository):

    def __init__(self, connection: Connection) -> None:
        self.connection = connection
    
    async def get_filmophile_achievements_policy(self) -> FilmophileAchievementsPolicy:
        data = await self.connection.fetchrow(
            "SELECT fap.* FROM filmophile_achievements_policy fap"
        )

        processed_data = {}
        for filmophile_achievement_policy_record in data:
            filmophile_achievement_policy = dict(filmophile_achievement_policy_record)
            rank = f"rank_{filmophile_achievement_policy['rank']}"
            rules = {"rated_movie_count": filmophile_achievement_policy_record["rated_movie_count"]}
            processed_data.update({rank: rules})

        return as_domain_policy(FilmophileAchievementsPolicy, data)