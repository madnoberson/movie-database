from dataclasses import dataclass
from datetime import date
from uuid import UUID


@dataclass(frozen=True, slots=True)
class AddMovieCommand:

    title: str
    release_date: date

    def __post_init__(self) -> None:
        is_valid = (
            isinstance(self.title, str) and
            len(self.title) > 0 and
            isinstance(self.release_date, date)
        )
        if not is_valid:
            raise ValueError()


@dataclass(frozen=True, slots=True)
class AddMovieCommandResult:

    movie_id: UUID
    