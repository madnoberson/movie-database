from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from .model import Model


@dataclass(slots=True)
class User(Model):

    id: UUID
    username: str
    password: str
    rated_movie_count: int
    created_at: datetime

    @classmethod
    def create(
        cls, user_id: UUID, username: str,
        password: str, created_at: datetime
    ) -> "User":
        return User(
            id=user_id, username=username,
            password=password, rated_movie_count=0,
            created_at=created_at
        )
    
    def change_username(self, username: str) -> None:
        self.username = username
    
    def change_password(self, password: str) -> None:
        self.password = password
    
    def add_movie_rating(self) -> None:
        self.rated_movie_count += 1
    
    def remove_movie_rating(self) -> None:
        self.rated_movie_count -= 1