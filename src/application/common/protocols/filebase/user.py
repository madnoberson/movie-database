from abc import abstractmethod
from typing import Protocol
from io import BytesIO


class SupportsUpdateUserAvatar(Protocol):

    @abstractmethod
    async def update_user_avatar(self, key: str, avatar: BytesIO) -> None:
        raise NotImplementedError