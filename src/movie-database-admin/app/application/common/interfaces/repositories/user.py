from abc import ABC, abstractmethod

from app.domain.models.user import User


class UserRepository(ABC):

    @abstractmethod
    async def check_user_exists(self, username: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def save_user(self, user: User) -> None:
        raise NotImplementedError
    