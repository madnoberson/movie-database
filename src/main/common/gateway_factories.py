from abc import ABC, abstractmethod
from typing import AsyncContextManager

from src.application.common.interfaces.database_gateway import DatabaseGateway


class GatewayFactory(ABC):

    @abstractmethod
    async def create_gateway(self) -> AsyncContextManager:
        raise NotImplementedError


class DatabaseGatewayFactory(GatewayFactory, ABC):

    @abstractmethod
    async def create_gateway(self) -> AsyncContextManager[DatabaseGateway]:
        raise NotImplementedError