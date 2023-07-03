from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional
from datetime import date

from .value_objects import (
    MovieId,
    MovieTitle,
    MoviePosterKey
)
from .constants import (
    MovieStatusEnum,
    MovieGenreEnum,
    MPAAEnum
)


@dataclass(slots=True)
class Movie:

    id: MovieId
    title: MovieTitle
    release_date: date
    rating: float
    rating_count: int

    status: MovieStatusEnum | None = None
    genres: list[MovieGenreEnum] = field(
        default_factory=list
    )
    mpaa: MPAAEnum | None = None
    poster_key: MoviePosterKey | None = None

    @classmethod
    def create(
        cls,
        id: MovieId,
        title: MovieTitle,
        release_date: date,
        status: Optional[MovieStatusEnum] = None,
        genres: list[MovieGenreEnum] = [],
        mpaa: Optional[MPAAEnum] = None,
        poster_key: Optional[MoviePosterKey] = None
    ) -> Movie:
        return Movie(
            id=id,
            title=title,
            release_date=release_date,
            rating=0,
            rating_count=0,
            status=status,
            genres=genres,
            mpaa=mpaa,
            poster_key=poster_key
        )
    
    def add_rating(self, rating: int | float) -> None:
        if not self.rating:
            self.rating = rating
            self.rating_count = 1
            return
        
        new_rating = (
            (self.rating * self.rating_count) + rating
        )
        self.rating_count += 1
        self.rating = new_rating / self.rating_count

    def remove_rating(self, rating: int | float) -> None:
        if not self.rating:
            return
        
        new_rating = (
            (self.rating * self.rating_count) - rating
        )

        self.rating_count -= 1
        if self.rating_count:
            self.rating = new_rating / self.rating_count
        else:
            self.rating = 0
    