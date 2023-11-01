from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.models.user import User


class UserRepository(ABC):

    @abstractmethod
    async def check_user_exists(self, username: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def save_user(self, user: User) -> None:
        raise NotImplementedError
    
    @abstractmethod
    async def get_user(self, user_id: UUID) -> User | None:
        raise NotImplementedError
    
    @abstractmethod
    async def update_user(self, user: User) -> None:
        raise NotImplementedError