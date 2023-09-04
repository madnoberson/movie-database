from abc import abstractmethod
from typing import Protocol
from io import BytesIO


class SupportsSavePersonAvatar(Protocol):

    @abstractmethod
    async def save_person_avatar(self, key: str, avatar: BytesIO) -> None:
        raise NotImplementedError


class SupportsUpdatePersonAvatar(Protocol):

    @abstractmethod
    async def update_person_avatar(self, key: str, avatar: BytesIO) -> None:
        raise NotImplementedError