from dataclasses import dataclass
from datetime import timedelta

from .model import Model


@dataclass(slots=True)
class MoviesRatingPolicy(Model):

    required_rated_movies_count: int
    required_time_pass_after_registration: timedelta
