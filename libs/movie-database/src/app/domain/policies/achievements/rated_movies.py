from dataclasses import dataclass

from app.domain.policies.policy import Policy


@dataclass(slots=True)
class RatedMoviesAchievementsPolicy(Policy):

    required_rated_movies_for_1_rank: int
    required_rated_movies_for_2_rank: int
    required_rated_movies_for_3_rank: int
    required_rated_movies_for_4_rank: int