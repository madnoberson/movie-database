from dataclasses import dataclass
from datetime import timedelta

from app.domain.policies.policy import Policy


@dataclass(slots=True)
class MoviesRatingPolicy(Policy):

    required_rated_movie_count: int
    required_days_pass_after_registration: timedelta
