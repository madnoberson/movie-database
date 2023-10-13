from abc import abstractmethod
from typing import Protocol


class UnitOfWork(Protocol):

    @abstractmethod
    async def commit(self) -> None:
        raise NotImplementedError
    
    @abstractmethod
    async def rollback(self) -> None:
        raise NotImplementedError