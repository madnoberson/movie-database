from abc import abstractmethod
from typing import Protocol


class SupportsCommit(Protocol):

    @abstractmethod
    async def commit(self) -> None:
        raise NotImplementedError