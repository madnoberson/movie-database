from abc import ABC, abstractmethod

from app.domain.policies.achievements import RatedMoviesAchievementsPolicy


class RatedMoviesAchievementsPolicyRepository(ABC):

    @abstractmethod
    async def get_rated_movies_achievements_policy(
        self
    ) -> RatedMoviesAchievementsPolicy:
        raise NotImplementedError