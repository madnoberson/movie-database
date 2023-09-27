import asyncio
from typing import AsyncIterator, AsyncContextManager
from contextlib import asynccontextmanager
from dataclasses import dataclass, field

from src.presentation.common.gateway_factory import GatewayFactory
from src.presentation.telegram.common.handler_factory import Handler, HandlerFactory


__all__ = ["HandlerFactoryImpl"]


@dataclass(frozen=True, slots=True)
class HandlerFactoryImpl(HandlerFactory[Handler]):

    handler: Handler
    dependencies: dict[str, object] = field(default_factory=dict)
    factories: dict[str, GatewayFactory] = field(default_factory=dict)

    @asynccontextmanager
    async def create_handler(self) -> AsyncIterator[Handler]:
        opened_context_managers = []
        try:
            gateways, context_managers = await create_gateways(self.factories)
            opened_context_managers.extend(context_managers)
            self.dependencies.update(gateways)
            yield self.handler(**self.dependencies)
        finally:
            await close_context_managers(opened_context_managers)


async def create_gateways(
    factories: dict[str, GatewayFactory]
) -> tuple[dict[str, object], list[AsyncContextManager]]:
    """
    Creates gateways from gateway factories and returns them and opened
    context managers
    """
    gateways, context_managers = {}, []
    for factory_name, factory in factories.items():
        context_manager = factory.create_gateway()
        context_managers.append(context_manager)
        gateway = await context_manager.__aenter__()
        gateways.update({factory_name: gateway})
    return gateways, context_managers


async def close_context_managers(context_managers: list[AsyncContextManager]) -> None:
    await asyncio.gather(*[cm.__aexit__(None, None, None) for cm in context_managers])
