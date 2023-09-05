from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass(frozen=True, slots=True)
class User:

    id: UUID
    username: str
    encoded_password: str
    created_at: datetime

    @classmethod
    def create(
        cls, user_id: UUID, username: str, encoded_password: str,
        created_at: datetime
    ) -> "User":
        return User(
            id=user_id, username=username, encoded_password=encoded_password,
            created_at=created_at
        )
