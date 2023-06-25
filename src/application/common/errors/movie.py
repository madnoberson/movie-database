from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True, slots=True)
class MovieDoesNotExistError(Exception):

    movie_id: UUID