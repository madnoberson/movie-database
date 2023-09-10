from typing import TypeVar, Generic, Callable, AsyncContextManager
from abc import ABC, abstractmethod


Interactor = TypeVar("Interactor")


class InteractorFactory(ABC, Generic[Interactor]):
    
    @abstractmethod
    async def create_interactor(self) -> AsyncContextManager[Interactor]:
        raise NotImplementedError
