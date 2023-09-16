from abc import ABC, abstractmethod
from typing import AsyncContextManager

from src.application.common.interfaces.db_gateway import DatabaseGateway
from src.application.common.interfaces.dbq_gateway import DatabaseQueriesGateway


class GatewayFactory(ABC):

    @abstractmethod
    async def create_gateway(self) -> AsyncContextManager:
        raise NotImplementedError


class DatabaseGatewayFactory(GatewayFactory, ABC):

    @abstractmethod
    async def create_gateway(self) -> AsyncContextManager[DatabaseGateway]:
        raise NotImplementedError


class DatabaseQueriesGatewayFactory(GatewayFactory, ABC):

    @abstractmethod
    async def create_gateway(self) -> AsyncContextManager[DatabaseQueriesGateway]:
        raise NotImplementedError