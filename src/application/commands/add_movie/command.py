from dataclasses import dataclass
from typing import Optional
from datetime import date
from io import BytesIO
from uuid import UUID

from src.domain.models.movie.constants import (
    MovieStatusEnum,
    MovieGenreEnum,
    MPAAEnum
)


@dataclass(frozen=True, slots=True)
class AddMovieCommand:

    title: str
    release_date: date
    
    status: Optional[MovieStatusEnum] = None
    genres: Optional[list[MovieGenreEnum]] = None
    mpaa: Optional[MPAAEnum] = None
    poster: Optional[BytesIO] = None

    def __post_init__(self) -> None:
        # FIXME: Kinda ugly. Simplify this for better readability
        is_valid = (
            isinstance(self.title, str) and
            len(self.title) > 0 and
            isinstance(self.release_date, date) and
            (isinstance(self.poster, BytesIO) or self.poster is None) and
            (isinstance(self.status, MovieStatusEnum) or self.status is None) and
            (   
                self.genres is None or
                isinstance(self.genres, list) and
                len(self.genres) == len(set(self.genres)) and
                all(map(lambda v: isinstance(v, MovieGenreEnum), self.genres))
            ) and
            (isinstance(self.mpaa, MPAAEnum) or self.mpaa is None)
        )
        if not is_valid:
            raise ValueError()


@dataclass(frozen=True, slots=True)
class AddMovieCommandResult:

    movie_id: UUID
    