from dataclasses import dataclass
from datetime import date
from uuid import UUID


@dataclass(frozen=True, slots=True)
class AddMovieCommand:

    title: str
    release_date: date


@dataclass(frozen=True, slots=True)
class AddMovieCommandResult:

    movie_id: UUID
    