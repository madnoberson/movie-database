from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime

from .value_objects import UserId, Username


@dataclass(slots=True)
class User:

    id: UserId
    username: Username
    password: str
    created_at: datetime

    @classmethod
    def create(
        cls,
        user_id: UserId,
        username: Username,
        password: str,
        created_at: datetime
    ) -> User:
        return User(
            id=user_id,
            username=username,
            password=password,
            created_at=created_at
        )

    def change_username(
        self,
        username: Username
    ) -> None:
        self.username = username
