from dataclasses import dataclass

from app.domain.policies.policy import Policy


@dataclass(slots=True)
class FilmophileAchievementRules:

    rated_movie_count: int


@dataclass(slots=True)
class FilmophileAchievementsPolicy(Policy):

    rank_1: FilmophileAchievementRules
    rank_2: FilmophileAchievementRules
    rank_3: FilmophileAchievementRules
    rank_4: FilmophileAchievementRules