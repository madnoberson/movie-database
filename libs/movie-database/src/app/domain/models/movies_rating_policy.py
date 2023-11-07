from dataclasses import dataclass
from datetime import timedelta

from .model import Model


@dataclass(slots=True)
class MoviesRatingPolicy(Model):

    required_rated_movie_count: int
    required_days_pass_after_registration: timedelta
