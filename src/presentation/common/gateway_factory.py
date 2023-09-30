from typing import TypeVar, Generic, AsyncContextManager
from abc import ABC, abstractmethod


Gateway = TypeVar("Gateway")


class GatewayFactory(ABC, Generic[Gateway]):

    @abstractmethod
    async def create_gateway(self) -> AsyncContextManager[Gateway]:
        raise NotImplementedError
