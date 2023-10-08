from abc import abstractmethod
from typing import Protocol

from app.application.common.query_results import auth


class SupportsLogin(Protocol):

    @abstractmethod
    async def login(self, username: str) -> auth.Login:
        raise NotImplementedError