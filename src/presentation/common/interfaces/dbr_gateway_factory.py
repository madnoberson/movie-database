from abc import ABC, abstractmethod
from typing import AsyncContextManager, TypeVar, Generic

from src.application.common.interfaces.dbr_gateway import DatabaseReadingGateway
from .gateway_factory import GatewayFactory


DBG = TypeVar("DBG", bound=DatabaseReadingGateway)


class DatabaseReadingGatewayFactory(GatewayFactory, ABC, Generic[DBG]):

    @abstractmethod
    async def create_gateway(self) -> AsyncContextManager[DBG]:
        raise NotImplementedError