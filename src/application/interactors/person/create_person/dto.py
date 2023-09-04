from dataclasses import dataclass
from datetime import date
from io import BytesIO
from uuid import UUID


@dataclass(frozen=True, slots=True)
class CreatePersonDTO:

    first_name: str
    last_name: str
    
    avatar: BytesIO | None = None
    birth_date: date | None = None
    birth_place: str | None = None
    death_date: date | None = None
    death_place: str | None = None
    kinopoisk_id: str | None = None
    imdb_id: str | None = None


@dataclass(frozen=True, slots=True)
class CreatePersonResultDTO:

    person_id: UUID