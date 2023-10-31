from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from .event import Event


@dataclass(frozen=True, slots=True)
class UserCreated(Event):

    user_id: UUID
    username: str
    created_at: datetime


@dataclass(frozen=True, slots=True)
class UsernameChanged(Event):

    user_id: UUID
    new_username: str