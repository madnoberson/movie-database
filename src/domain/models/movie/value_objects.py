from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True, slots=True)
class MovieId:

    value: UUID


@dataclass(frozen=True, slots=True)
class MovieTitle:

    value: str


@dataclass(frozen=True, slots=True)
class MovieRating:

    rating: int
    rating_count: int
    