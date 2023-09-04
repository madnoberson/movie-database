import asyncio
from logging import getLogger
from dataclasses import dataclass
from datetime import datetime

from src.domain.person import Person
from src.application.common import utils
from src.application.common import mixins
from . import dto
from . import errors
from . import interfaces


logger = getLogger("UpdatePerson")


@dataclass(frozen=True, slots=True)
class UpdatePerson(mixins.SupportsGetAndCachePerson):

    db_gateway: interfaces.DatabaseGateway
    cb_gateway: interfaces.CachebaseGateway
    fb_gateway: interfaces.FilebaseGateway

    @utils.handle_unexpected_exceptions(logger, errors.PersonDoesNotExistError)
    async def __call__(self, data: dto.UpdatePersonDTO) -> None:
        # 1.Get person
        person: Person = await self.get_and_cache_person(
            db_gateway=self.db_gateway, cb_gateway=self.cb_gateway,
            person_id=data.person_id, kinopoisk_id=data.kinopoisk_id,
            imdb_id=data.imdb_id
        )
        if person is None:
            raise errors.PersonDoesNotExistError()
        
        # 2.Update person
        person.update(
            updated_at=datetime.utcnow(), first_name=data.first_name,
            last_name=data.last_name, movie_count=data.movie_count,
            career=data.career, genres=data.genres,
            avatar_url=f"{person.id.hex}-person_avatar" if data.avatar else None,
            birth_date=data.birth_date, birth_place=data.birth_place,
            death_date=data.death_date, death_place=data.death_place,
            kinopoisk_id=data.new_kinopoisk_id, imdb_id=data.new_imdb_id
        )

        # 3.Save changes
        if data.avatar is not None:
            await asyncio.gather(
                self.db_gateway.update_person(person), self.cb_gateway.update_person(person),
                self.fb_gateway.update_person_avatar(key=person.avatar_url, avatar=data.avatar)
            )
            await asyncio.gather(
                self.db_gateway.commit(), self.cb_gateway.commit(), self.fb_gateway.commit()
            )
        else:
            await asyncio.gather(
                self.db_gateway.update_person(person), self.cb_gateway.update_person(person)
            )
            await asyncio.gather(
                self.db_gateway.commit(), self.cb_gateway.commit()
            )
        
