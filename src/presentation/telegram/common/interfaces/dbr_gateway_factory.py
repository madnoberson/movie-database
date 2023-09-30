from abc import ABC, abstractmethod
from typing import AsyncContextManager

from src.application.common.interfaces.dbr_gateway import DatabaseReadingGateway
from src.presentation.common.gateway_factory import GatewayFactory


class DatabaseReadingGatewayFactory(GatewayFactory[DatabaseReadingGateway], ABC):

    @abstractmethod
    async def create_gateway(self) -> AsyncContextManager[DatabaseReadingGateway]:
        raise NotImplementedError