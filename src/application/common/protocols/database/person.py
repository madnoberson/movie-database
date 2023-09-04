from typing import overload, Protocol
from abc import abstractmethod
from uuid import UUID

from src.domain.person import Person


class SupportsSavePerson(Protocol):

    @abstractmethod
    async def save_person(self, person: Person) -> None:
        raise NotImplementedError


class SupportsGetPerson(Protocol):

    @overload
    async def get_person(self, kinopoisk_id: str) -> Person | None:
        raise NotImplementedError

    @overload
    async def get_person(self, imdb_id: str) -> Person | None:
        raise NotImplementedError

    @overload
    async def get_person(self, person_id: UUID) -> Person | None:
        raise NotImplementedError

    @abstractmethod
    async def get_person(
        self, kinoposk_id: str | None = None, imdb_id: str | None = None,
        person_id: UUID | None = None
    ) -> Person | None:
        raise NotImplementedError


class SupportsUpdatePerson(Protocol):

    @abstractmethod
    async def update_person(self, person: Person) -> None:
        raise NotImplementedError