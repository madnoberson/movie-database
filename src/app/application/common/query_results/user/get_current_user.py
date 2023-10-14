from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass(frozen=True, slots=True)
class Data:

    user_id: UUID
    username: str
    created_at: datetime


@dataclass(frozen=True, slots=True)
class GetCurrentUser:

    data: Data
