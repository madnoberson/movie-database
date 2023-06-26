from __future__ import annotations
from dataclasses import dataclass
from datetime import date

from .value_objects import (
    MovieId,
    MovieTitle
)


@dataclass(slots=True)
class Movie:

    id: MovieId
    title: MovieTitle
    release_date: date
    rating: float
    rating_count: int

    @classmethod
    def create(
        cls,
        id: MovieId,
        title: MovieTitle,
        release_date: date
    ) -> Movie:
        return Movie(
            id=id,
            title=title,
            release_date=release_date,
            rating=0,
            rating_count=0
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
        self.rating = new_rating / self.rating_count
    