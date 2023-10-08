from abc import ABC, abstractmethod
from typing import AsyncContextManager, TypeVar, Generic

from app.application.common.interfaces.dbw_gateway import DatabaseWritingGateway
from .gateway_factory import GatewayFactory


DBW = TypeVar("DBW", bound=DatabaseWritingGateway)


class DatabaseWritingGatewayFactory(GatewayFactory, ABC, Generic[DBW]):

    @abstractmethod
    async def create_gateway(self) -> AsyncContextManager[DBW]:
        raise NotImplementedError