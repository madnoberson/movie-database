from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True, slots=True)
class UserMovieRatingAlreadyExists(Exception):

    movie_id: UUID
    