from abc import ABC, abstractmethod

from app.domain.policies.achievements import FilmophileAchievementsPolicy


class FilmophileAchievementsPolicyRepository(ABC):

    @abstractmethod
    async def get_filmophile_achievements_policy(
        self
    ) -> FilmophileAchievementsPolicy:
        raise NotImplementedError