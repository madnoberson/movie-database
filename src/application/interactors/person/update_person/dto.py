from dataclasses import dataclass
from datetime import date
from io import BytesIO
from uuid import UUID

from src.domain.person import PersonCareer
from src.domain.movie import MovieGenreEnum


@dataclass(frozen=True, slots=True)
class UpdatePersonDTO:

    person_id: UUID | None = None
    imdb_id: str | None = None
    kinopoisk_id: str | None = None

    first_name: str | None = None
    last_name: str | None = None
    movie_count: int | None = None
    career: list[PersonCareer] | None = None
    genres: list[MovieGenreEnum] | None = None
    avatar: str | None = None
    birth_date: date | None = None
    birth_place: str | None = None
    death_date: date | None = None
    death_place: str | None = None
    new_kinopoisk_id: str | None = None
    new_imdb_id: str | None = None