from dataclasses import dataclass
from datetime import datetime, date
from typing import Sequence
from uuid import UUID

from .crew_member import CrewMemberRoleEnum
from .movie import MovieGenreEnum


@dataclass(frozen=True, slots=True)
class PersonCareer:

    role: CrewMemberRoleEnum
    movie_count: int
    genres: Sequence[MovieGenreEnum]


@dataclass(slots=True)
class Person:

    id: UUID
    first_name: str
    last_name: str
    created_at: datetime
    
    movie_count: int | None
    career: PersonCareer | None
    genres: Sequence[MovieGenreEnum] | None
    avatar_url: str | None
    birth_date: date | None
    birth_place: str | None
    death_date: date | None
    death_place: str | None
    kinopoisk_id: str | None
    imdb_id: str | None
    updated_at: datetime | None

    @classmethod
    def create(
        cls, person_id: UUID, created_at: datetime, first_name: str,
        last_name: str, career: PersonCareer | None = None,
        genres: Sequence[MovieGenreEnum] | None = None,
        movie_count: int | None = None, avatar_url: str | None = None,
        birth_date: date | None = None, birth_place: str | None = None,
        death_date: date | None = None, death_place: str | None = None,
        kinopoisk_id: str | None = None, imdb_id: str | None = None
    ) -> "Person":
        return Person(
            id=person_id, first_name=first_name, last_name=last_name,
            created_at=created_at, career=career, genres=genres,
            movie_count=movie_count, avatar_url=avatar_url, birth_date=birth_date,
            birth_place=birth_place, death_date=death_date, death_place=death_place,
            kinopoisk_id=kinopoisk_id, imdb_id=imdb_id, updated_at=None
        )