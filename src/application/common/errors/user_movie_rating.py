from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True, slots=True)
class UserMovieRatingDoesNotExistError(Exception):
    
    movie_id: UUID
    