import asyncio
from logging import getLogger
from dataclasses import dataclass
from datetime import datetime
from uuid import uuid4

from src.domain.person import Person
from src.application.common import utils
from src.application.common import mixins
from . import dto
from . import errors
from . import interfaces


logger = getLogger("CreatePerson")


@dataclass(frozen=True, slots=True)
class CreatePerson(mixins.SupportsGetAndCachePerson):

    db_gateway: interfaces.DatabaseGateway
    cb_gateway: interfaces.CachebaseGateway
    fb_gateway: interfaces.FilebaseGateway
    tq_gateway: interfaces.TaskQueueGateway

    @utils.handle_unexpected_exceptions(logger, errors.PersonAlreadyExistsError)
    async def __call__(self, data: dto.CreatePersonDTO) -> dto.CreatePersonResultDTO:
        # 1.Ensure person doesn't exist
        if data.kinopoisk_id is not None or data.imdb_id is not None:
            person = await self.get_and_cache_person(
                db_gateway=self.db_gateway, cb_gateway=self.cb_gateway,
                kinopoisk_id=data.kinopoisk_id, imdb_id=data.imdb_id
            )
            if person is not None:
                raise errors.PersonAlreadyExistsError()
        
        # 2.Create person
        person_id = uuid4()
        person = Person.create(
            person_id=person_id, created_at=datetime.utcnow(),
            first_name=data.first_name, last_name=data.last_name,
            birth_date=data.birth_date, birth_place=data.birth_place,
            death_date=data.death_date, death_place=data.death_place,
            kinopoisk_id=data.kinopoisk_id, imdb_id=data.imdb_id,
            avatar_url=f"{person_id.hex}-person_avatar" if data.avatar else None
        )

        # 3.Save person and enqueue `fill_person_data` task
        if data.avatar is not None:
            await asyncio.gather(
                self.db_gateway.save_person(person), self.cb_gateway.save_person(person),
                self.fb_gateway.save_person_avatar(key=person.avatar_url, avatar=data.avatar),
                self.tq_gateway.enqueue_fill_person_data_task(person_id=person.id)
            )
            await asyncio.gather(
                self.db_gateway.commit(), self.cb_gateway.commit(), self.fb_gateway.commit(),
                self.tq_gateway.commit()
            )
        else:
            await asyncio.gather(
                self.db_gateway.save_person(person), self.cb_gateway.save_person(person),
                self.tq_gateway.enqueue_fill_person_data_task(person_id=person.id)
            )
            await asyncio.gather(
                self.db_gateway.commit(), self.cb_gateway.commit(), self.tq_gateway.commit()
            )
        
        return dto.CreatePersonResultDTO(person_id=person.id)
