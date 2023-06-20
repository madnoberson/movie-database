from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime

from .value_objects import (
    MovieId,
    MovieTitle,
    MovieRating
)


@dataclass(slots=True)
class Movie:

    id: MovieId
    title: MovieTitle
    rating: MovieRating
    release_date: datetime

    @classmethod
    def create(
        cls,
        id: MovieId,
        title: MovieTitle,
        release_date: datetime
    ) -> Movie:
        return Movie(
            id=id,
            title=title,
            rating=MovieRating(0, 0),
            release_date=release_date
        )
