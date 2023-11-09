from asyncpg.connection import Connection

from app.domain.policies import FilmophileAchievementsPolicy
from app.application.common.interfaces.repositories import FilmophileAchievementsPolicyRepository
from app.infrastructure.database.mappers import as_domain_policy


class FilmophileAchievementsPolicyRepositoryImpl(FilmophileAchievementsPolicyRepository):

    def __init__(self, connection: Connection) -> None:
        self.connection = connection
    
    async def get_filmophile_achievements_policy(self) -> FilmophileAchievementsPolicy:
        data = await self.connection.fetch("SELECT fa.* FROM filmophile_achievements fa")

        filmophile_achievements_policy_data = {}
        for filmophile_achievement_data, rank in zip(data, range(1, 5)):
            rated_movie_count = dict(filmophile_achievement_data)["required_rated_movie_count"]
            filmophile_achievement_rules = {"rated_movie_count": rated_movie_count}
            filmophile_achievements_policy_data[f"rank_{rank}"] = filmophile_achievement_rules

        return as_domain_policy(FilmophileAchievementsPolicy, filmophile_achievements_policy_data)