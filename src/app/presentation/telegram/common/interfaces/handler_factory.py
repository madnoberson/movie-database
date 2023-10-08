from typing import TypeVar, Generic, Callable, AsyncContextManager
from abc import ABC, abstractmethod


H = TypeVar("H", bound=Callable[[object], object])


class HandlerFactory(ABC, Generic[H]):
    
    @abstractmethod
    async def create_handler(self) -> AsyncContextManager[H]:
        """
        Setups dependencies to handler and returns it.
        
        Example:

        .. code-block::python
        async with some_handler_factory.create_handler() as handle:
            await handle(SomeHandlerDTO()) 
        """
        raise NotImplementedError