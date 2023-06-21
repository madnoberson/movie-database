from abc import abstractmethod
from typing import Protocol

from src.domain.models.user.model import User
from src.domain.models.user.value_objects import UserId, Username


class SupportsGetUserById(Protocol):

    @abstractmethod
    def get_user_by_id(self, user_id: UserId) -> User | None:
        raise NotImplementedError


class SupportsGetUserByUsername(Protocol):

    @abstractmethod
    def get_user_by_username(self, username: Username) -> User | None:
        raise NotImplementedError


class SupportsSaveUser(Protocol):

    @abstractmethod
    def save_user(self, user: User) -> None:
        raise NotImplementedError