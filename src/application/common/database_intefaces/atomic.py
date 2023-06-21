from abc import abstractmethod
from typing import Protocol


class SupportsAtomic(Protocol):
    
    @abstractmethod
    def commit(self) -> None:
        raise NotImplementedError
    
    @abstractmethod
    def rollback(self) -> None:
        raise NotImplementedError
    