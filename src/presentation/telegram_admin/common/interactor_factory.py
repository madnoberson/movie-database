from typing import TypeVar, Generic, AsyncContextManager
from abc import ABC, abstractmethod


Interactor = TypeVar("Interactor")


class InteractorFactory(ABC, Generic[Interactor]):
    
    @abstractmethod
    async def create_interactor(self) -> AsyncContextManager[Interactor]:
        """
        Setups dependencies to interactor and returns it.
        
        Example:

        .. code-block::python
        async with interactor_factory.create_interactor() as execute:
            await exectue(InteractorDTO()) 
        """
        raise NotImplementedError
