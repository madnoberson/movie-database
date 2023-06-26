from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True, slots=True)
class ReevaluateMovieCommand:

    user_id: UUID
    movie_id: UUID
    new_rating: float | int

    def __post_init__(self) -> None:
        is_valid = (
            isinstance(self.user_id, UUID) and
            isinstance(self.movie_id, UUID) and
            isinstance(self.new_rating, (float, int)) and
            0 < self.new_rating <= 10 and
            self.new_rating % 0.5 == 0
        )
        if not is_valid:
            raise ValueError()


@dataclass(frozen=True, slots=True)
class ReevaluateMovieCommandResult:

    new_user_rating: float | int
    new_movie_rating: float | int 
    new_movie_rating_count: int
    