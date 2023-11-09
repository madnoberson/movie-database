from dataclasses import dataclass

from app.domain.policies.policy import Policy


@dataclass(slots=True)
class FilmophileAchievementConditions:

    rated_movie_count: int


@dataclass(slots=True)
class FilmophileAchievementsPolicy(Policy):

    rank_1: FilmophileAchievementConditions
    rank_2: FilmophileAchievementConditions
    rank_3: FilmophileAchievementConditions
    rank_4: FilmophileAchievementConditions