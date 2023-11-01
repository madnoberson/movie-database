from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from .model import Model


@dataclass(slots=True)
class User(Model):

    id: UUID
    username: str
    password: str
    created_at: datetime

    @classmethod
    def create(
        cls, user_id: UUID, username: str,
        password: str, created_at: datetime
    ) -> "User":
        return User(
            id=user_id, username=username,
            password=password, created_at=created_at
        )
    
    def change_username(self, username: str) -> None:
        self.username = username
    
    def change_password(self, password: str) -> None:
        self.password = password