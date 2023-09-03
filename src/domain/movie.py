from dataclasses import dataclass
from datetime import datetime, date
from typing import Sequence
from enum import IntEnum
from uuid import UUID


class MovieStatusEnum(IntEnum):

    RELEASED = 0
    CANCELED = 1
    PLANNED = 2


class MPAAEnum(IntEnum):

    G = 0
    PG = 1
    PG13 = 2
    R = 3
    NC17 = 4


class MovieGenreEnum(IntEnum):

    ACTION = 0
    THRILLER = 1
    COMEDY = 2
    WAR = 3
    DOCUMENTARY = 4
    CRIME = 5
    DRAMA = 6
    ROMANCE = 7
    FANTASY = 8
    ADVENTURE = 9
    HORROR = 10
    MUSICAL = 11
    MYSTERY = 12
    SCIENCE_FICTION = 13
    WESTERN = 14
    HISTORY = 15
    BIOGRAPHY = 16
    ANIMATION = 17


@dataclass(slots=True)
class Movie:

    id: UUID
    title: str
    release_date: date
    director_ids: Sequence[UUID]
    writer_ids: Sequence[UUID]
    producer_ids: Sequence[UUID]
    composer_ids: Sequence[UUID]
    editor_ids: Sequence[UUID]
    actors_ids: Sequence[UUID]
    genres: Sequence[MovieGenreEnum]
    rating_count: int
    created_at: datetime
    
    status: MovieStatusEnum | None
    poster_url: str | None
    mpaa: MPAAEnum | None
    budget: int | None
    revenue: int | None
    rating: float | None
    kinopoisk_rating: float | None
    imdb_rating: float | None
    updated_at: datetime | None

    @classmethod
    def create(
        cls, movie_id: UUID, title: str, release_date: date,
        director_ids: Sequence[UUID], writer_ids: Sequence[UUID],
        producer_ids: Sequence[UUID], composer_ids: Sequence[UUID],
        editor_ids: Sequence[UUID], actor_ids: Sequence[UUID],
        genres: Sequence[MovieGenreEnum], created_at: datetime,
        status: MovieStatusEnum | None = None, poster_url: str | None = None,
        mpaa: MPAAEnum | None = None, budget: int | None = None,
        revenue: int | None = None, kinopoisk_rating: float | None = None,
        imdb_rating: float | None = None
    ) -> "Movie":
        return Movie(
            id=movie_id, title=title, release_date=release_date,
            director_ids=director_ids, writer_ids=writer_ids,
            producer_ids=producer_ids, composer_ids=composer_ids,
            editor_ids=editor_ids, actors_ids=actor_ids,
            genres=genres, rating_count=0, created_at=created_at,
            status=status, poster_url=poster_url, mpaa=mpaa,
            budget=budget, revenue=revenue, rating=None,
            kinopoisk_rating=kinopoisk_rating, imdb_rating=imdb_rating,
            updated_at=None
        )