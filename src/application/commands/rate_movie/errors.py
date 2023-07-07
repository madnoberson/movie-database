from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True, slots=True)
class UserMovieRatingAlreadyExistsError(Exception):

    movie_id: UUID

    @property
    def message(self) -> str:
        return f"Movie rating already exists"
    