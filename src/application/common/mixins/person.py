from typing import overload, Protocol
from uuid import UUID

from src.domain.person import Person
from src.application.common.protocols.database import person as person_db
from src.application.common.protocols.cachebase import atomacity as atomacity_cb
from src.application.common.protocols.cachebase import person as person_cb


__all__ = ["SupportsGetAndCachePerson"]


class DatabaseGateway(
    person_db.SupportsGetPerson,
    Protocol
):
    ...


class CachebaseGateway(
    atomacity_cb.SupportsCommit,
    person_cb.SupportsGetPerson,
    person_cb.SupportsSavePerson,
    Protocol
):
    ...


class SupportsGetAndCachePerson:

    @overload
    async def get_and_cache_person(
        self, db_gateway: DatabaseGateway, cb_gateway: CachebaseGateway,
        kinopoisk_id: str
    ) -> Person | None:
        ...
    
    @overload
    async def get_and_cache_person(
        self, db_gateway: DatabaseGateway, cb_gateway: CachebaseGateway,
        imdb_id: str
    ) -> Person | None:
        ...
    
    @overload
    async def get_and_cache_person(
        self, db_gateway: DatabaseGateway, cb_gateway: CachebaseGateway,
        person_id: UUID
    ) -> Person | None:
        ...
    
    async def get_and_cache_person(
        self, db_gateway: DatabaseGateway, cb_gateway: CachebaseGateway,
        kinopoisk_id: str | None = None, imdb_id: str | None = None,
        person_id: UUID | None = None
    ) -> Person | None:
        # 1.Get person from cachebase
        person = await cb_gateway.get_person(
            kinopoisk_id=kinopoisk_id, imdb_id=imdb_id, person_id=person_id
        )
        if person is not None: return person

        # 2.Get person from database if person not in cachebase
        person = await db_gateway.get_person(
            kinopoisk_id=kinopoisk_id, imdb_id=imdb_id, person_id=person_id
        )
        if person is not None:
            await cb_gateway.save_person(person)
            await cb_gateway.commit()
        
        return person