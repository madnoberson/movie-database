from abc import abstractmethod
from typing import Protocol
from uuid import UUID

from src.domain.user import User


class SupportsCheckUserExists(Protocol):

    @abstractmethod
    async def check_user_exists(self, email: str) -> bool:
        raise NotImplementedError


class SupportsSaveUser(Protocol):

    @abstractmethod
    async def save_user(self, user: User) -> None:
        raise NotImplementedError


class SupportsGetUser(Protocol):

    @abstractmethod
    async def get_user(self, user_id: UUID) -> User | None:
        raise NotImplementedError


class SupportsUpdateUser(Protocol):

    @abstractmethod
    async def update_user(self, user: User) -> None:
        raise NotImplementedError