from dataclasses import dataclass

from app.domain.policies.policy import Policy


@dataclass(slots=True)
class RatedMoviesAchievementRules:

    rated_movie_count: int


@dataclass(slots=True)
class RatedMoviesAchievementsPolicy(Policy):

    rank_1: RatedMoviesAchievementRules
    rank_2: RatedMoviesAchievementRules
    rank_3: RatedMoviesAchievementRules
    rank_4: RatedMoviesAchievementRules