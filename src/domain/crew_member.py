from dataclasses import dataclass
from datetime import datetime
from typing import Sequence
from enum import IntEnum
from uuid import UUID


class CrewMemberRoleEnum(IntEnum):

    DIRECTOR = 0
    ACTOR = 1
    WRITER = 2
    PRODUCER = 3
    COMPOSER = 4
    EDITOR = 5


@dataclass(slots=True)
class CrewMember:

    id: UUID
    person_id: UUID
    movie_id: UUID
    roles: Sequence[CrewMemberRoleEnum]
    created_at: datetime

    updated_at: datetime | None

    @classmethod
    def create(
        cls, crew_member_id: UUID, person_id: UUID,
        movie_id: UUID, roles: Sequence[CrewMemberRoleEnum],
        created_at: datetime
    ) -> "CrewMember":
        return CrewMember(
            id=crew_member_id, person_id=person_id, movie_id=movie_id,
            roles=roles, created_at=created_at, updated_at=None
        )
    
