from dataclasses import dataclass
from uuid import UUID

from .event import Event


@dataclass(frozen=True, slots=True)
class UsernameChanged(Event):

    user_id: UUID
    new_username: str