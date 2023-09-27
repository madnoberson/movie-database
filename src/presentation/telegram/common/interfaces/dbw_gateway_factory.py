from abc import ABC, abstractmethod
from typing import AsyncContextManager

from src.application.common.interfaces.dbw_gateway import DatabaseWritingGateway
from src.presentation.common.gateway_factory import GatewayFactory


class DatabaseWritingGatewayFactory(GatewayFactory[DatabaseWritingGateway], ABC):

    @abstractmethod
    async def create_gateway(self) -> AsyncContextManager[DatabaseWritingGateway]:
        raise NotImplementedError