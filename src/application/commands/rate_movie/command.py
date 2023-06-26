from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass(frozen=True, slots=True)
class RateMovieCommand:

    user_id: UUID
    movie_id: UUID
    rating: float | int

    def __post_init__(self) -> None:
        is_valid = (
            isinstance(self.user_id, UUID) and
            isinstance(self.movie_id, UUID) and
            isinstance(self.rating, (float, int)) and
            0 < self.rating <= 10 and
            self.rating % 0.5 == 0
        )
        if not is_valid:
            raise ValueError()


@dataclass(frozen=True, slots=True)
class RateMovieCommandResult:

    new_movie_rating: float | int
    new_movie_rating_count: int
    user_rating: float | int
    user_rating_created_at: datetime