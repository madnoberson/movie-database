import asyncio
from typing import AsyncContextManager, AsyncIterator
from dataclasses import dataclass, field
from contextlib import asynccontextmanager

from aiogram import Dispatcher

from src.application.common.interfaces.password_encoder import PasswordEncoder
from src.presentation.telegram.common.handler_factory import Handler, HandlerFactory
from src.main.common import gateway_factories


__all__ = ["setup_handler_factories"]


@dataclass(frozen=True, slots=True)
class HandleractoryImpl(HandlerFactory):
    
    handler: Handler
    factories: dict[str, gateway_factories.GatewayFactory] = field(default_factory=dict)
    dependencies: dict[str, object] = field(default_factory=dict)

    @asynccontextmanager
    async def create_handler(self) -> AsyncIterator[Handler]:
        """
        Setups dependencies to handler and returns it.
        
        Example:

        .. code-block::python
        from path_to_some_handler_dto import SomeHandlerDTO

        async with some_handler_factory.create_handler() as handle:
            await handle(SomeHandlerDTO()) 
        """
        opened_context_managers = []
        try:
            gateways, context_managers = await self.create_gateways(self.factories)
            opened_context_managers.extend(context_managers)
            self.dependencies.update(gateways)
            yield self.handler(**self.dependencies)
        finally:
            await self.close_context_managers(opened_context_managers)
    
    @staticmethod
    async def create_gateways(
        factories: dict[str, gateway_factories.GatewayFactory]
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

    @staticmethod
    async def close_context_managers(context_managers: list[AsyncContextManager]) -> None:
        coros = [
            context_manager.__aexit__(None, None, None)
            for context_manager in context_managers
        ]
        await asyncio.gather(*coros)


def setup_handler_factories(
    dispatcher: Dispatcher, handlers: list[Handler],
    db_gateway_factory: gateway_factories.DatabaseGatewayFactory, password_encoder: PasswordEncoder,
    dbq_gateway_factory: gateway_factories.DatabaseQueriesGatewayFactory
) -> None:
    """
    Setup dependency-injected handler factories to dispatcher.
    For Example `SomeHandler` will be wrapped in `HandlerFactory`
    and can be used in any aiogram function like this:

    .. code-block::python
    from path_to_some_handler import SomeHandler
    from path_to_some_handler_dto import SomeHandlerDTO

    async def aiogram_function(
        message: Message,
        some_handler_factory: HandlerFactory[SomeHandler]
        # Note: `SomeHandler` has become `some_handler_factory`
    ) -> None:
        async with some_handler_factory.create_handler() as handle:
            await handle(SomeHandlerDTO())
    """
    
    def create_handler_factory_name(handler: Handler) -> str:
        """
        Converts pascal case `handler` name into snake case with '_factory' at the end.
        For example `SomeHandler` will become `some_handler_factory`
        """
        handler_name = handler.__name__[0].lower() + handler.__name__[1:]
        handler_factory_name = ""
        for letter in handler_name:
            if letter.isupper():
                handler_factory_name += f"_{letter.lower()}"
                continue
            handler_factory_name += letter
        return handler_factory_name + "_factory"

    def create_handler_factory(handler: Handler) -> HandleractoryImpl:
        """Returns dependency-injected handler factory"""
        factory_overrides = {"db_gateway": db_gateway_factory, "pdb_gateway": dbq_gateway_factory}
        dependency_overrides = {"password_encoder": password_encoder}
        dependencies, factories = {}, {}
        for dependency_name in handler.__annotations__.keys():
            if dependency_name in factory_overrides:
                factories.update({dependency_name: factory_overrides[dependency_name]})
            elif dependency_name in dependency_overrides:
                dependencies.update({dependency_name: dependency_overrides[dependency_name]})
        return HandleractoryImpl(handler=handler, factories=factories, dependencies=dependencies)

    for handler in handlers:
        dispatcher[create_handler_factory_name(handler)] = create_handler_factory(handler)