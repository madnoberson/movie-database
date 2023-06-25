from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass(frozen=True, slots=True)
class RateMovieCommand:

    user_id: UUID
    movie_id: UUID
    rating: float


@dataclass(frozen=True, slots=True)
class RateMovieCommandResult:

    new_movie_rating: float
    user_rating: float
    user_rating_created_at: datetime