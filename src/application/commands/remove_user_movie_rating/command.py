from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True, slots=True)
class RemoveUserMovieRatingCommand:

    user_id: UUID
    movie_id: UUID

    def __post_init__(self) -> None:
        is_valid = (
            isinstance(self.user_id, UUID) and
            isinstance(self.movie_id, UUID)
        )
        if not is_valid:
            raise ValueError()


@dataclass(frozen=True, slots=True)
class RemoveUserMovieRatingCommandResult:

    new_movie_rating: float
    new_movie_rating_count: int
