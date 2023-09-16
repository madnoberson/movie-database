from abc import abstractmethod
from typing import Protocol

from src.application.common.query_results import profile as query_results


class SupportsCheckUsernameExists(Protocol):

    @abstractmethod
    async def check_username_exists(self, username: str) -> query_results.CheckUsernameExists:
        raise NotImplementedError