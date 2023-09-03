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
    career: PersonCareer
    genres: Sequence[MovieGenreEnum]
    movie_count: int
    created_at: datetime

    avatar_url: str | None
    birth_date: date | None
    birth_place: str | None
    death_date: date | None
    death_place: str | None
    updated_at: datetime | None

    @classmethod
    def create(
        cls, person_id: UUID, career: PersonCareer,
        genres: Sequence[MovieGenreEnum], movie_count: int,
        created_at: datetime, avatar_url: str | None = None,
        birth_date: date | None = None, birth_place: str | None = None,
        death_date: date | None = None, death_place: str | None = None
    ) -> "Person":
        return Person(
            id=person_id, career=career, genres=genres,
            movie_count=movie_count, created_at=created_at,
            avatar_url=avatar_url, birth_date=birth_date,
            birth_place=birth_place, death_date=death_date,
            death_place=death_place, updated_at=None
        )