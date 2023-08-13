from abc import abstractmethod
from typing import Protocol, overload
from uuid import UUID

from src.domain.user import User


class SupportsEnsureUserExists(Protocol):

    @overload
    async def ensure_user_exists(self, user_id: UUID) -> bool:
        raise NotImplementedError

    @overload
    async def ensure_user_exists(self, username: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def ensure_user_exists(
        self,
        user_id: UUID = None,
        username: str = None
    ) -> bool:
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


class SupportsDeleteUser(Protocol):

    @abstractmethod
    async def delete_user(self, user_id: UUID) -> None:
        raise NotImplementedError