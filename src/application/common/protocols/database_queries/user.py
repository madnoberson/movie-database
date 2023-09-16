from abc import abstractmethod
from typing import Protocol

from src.application.common.query_results import user as query_results


class SupportsCheckEmailExists(Protocol):

    @abstractmethod
    async def check_email_exists(self, email: str) -> query_results.CheckEmailExists:
        raise NotImplementedError