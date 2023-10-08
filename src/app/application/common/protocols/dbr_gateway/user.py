from abc import abstractmethod
from typing import Protocol

from app.application.common.query_results import user


class SupportsCheckUsernameExists(Protocol):

    @abstractmethod
    async def check_username_exists(self, username: str) -> user.CheckUsernameExists:
        raise NotImplementedError