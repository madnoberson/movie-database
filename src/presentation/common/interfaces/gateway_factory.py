from typing import TypeVar, Generic, AsyncContextManager
from abc import ABC, abstractmethod


G = TypeVar("G")


class GatewayFactory(ABC, Generic[G]):

    @abstractmethod
    async def create_gateway(self) -> AsyncContextManager[G]:
        raise NotImplementedError