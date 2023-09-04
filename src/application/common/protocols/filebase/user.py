from abc import abstractmethod
from typing import Protocol
from io import BytesIO


class SupportsSaveUserAvatar(Protocol):

    @abstractmethod
    async def save_user_avatar(self, key: str, avatar: BytesIO) -> None:
        raise NotImplementedError


class SupportsUpdateUserAvatar(Protocol):

    @abstractmethod
    async def update_user_avatar(self, key: str, avatar: BytesIO) -> None:
        raise NotImplementedError