from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass(slots=True)
class User:

    id: UUID
    username: str
    hashed_password: str
    created_at: datetime

    @classmethod
    def create(
        cls,
        user_id: UUID,
        username: str,
        hashed_password: str,
        created_at: datetime
    ) -> "User":
        return User(
            id=user_id,
            username=username,
            hashed_password=hashed_password,
            created_at=created_at
        )