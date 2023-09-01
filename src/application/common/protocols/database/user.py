from typing import Protocol, overload
from abc import abstractmethod
from uuid import UUID

from src.domain.user import User


class SupportsSaveUser(Protocol):

    @abstractmethod
    async def save_user(self, user: User) -> None:
        raise NotImplementedError


class SupportsGetUser(Protocol):

    @overload
    async def get_user(self, user_id: UUID) -> User | None:
        raise NotImplementedError

    @overload
    async def get_user(self, email: str) -> User | None:
        raise NotImplementedError
    
    @abstractmethod
    async def get_user(
        self, user_id: UUID | None = None, email: str | None = None
    ) -> User | None:
        raise NotImplementedError


class SupportsUpdateUser(Protocol):

    @abstractmethod
    async def update_user(self, user: User) -> None:
        raise NotImplementedError
