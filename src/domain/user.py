from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass(slots=True)
class User:

    id: UUID
    email: str
    username: str
    encoded_password: str
    created_at: datetime

    @classmethod
    def create(
        cls, user_id: UUID, email: str, username: str,
        encoded_password: str, created_at: str
    ) -> "User":
        return User(
            id=user_id, email=email, username=username,
            encoded_password=encoded_password, created_at=created_at
        )
    