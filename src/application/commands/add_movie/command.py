from dataclasses import dataclass, field
from typing import Optional
from datetime import date
from uuid import UUID


@dataclass(frozen=True, slots=True)
class AddMovieCommand:

    title: str
    release_date: date
    
    poster: Optional[bytes] = field(default=None)

    def __post_init__(self) -> None:
        is_valid = (
            isinstance(self.title, str) and
            len(self.title) > 0 and
            isinstance(self.release_date, date) and
            (isinstance(self.poster, bytes) or self.poster is None)
        )
        if not is_valid:
            raise ValueError()


@dataclass(frozen=True, slots=True)
class AddMovieCommandResult:

    movie_id: UUID
    