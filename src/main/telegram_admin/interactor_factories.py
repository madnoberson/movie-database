import asyncio
from typing import AsyncContextManager, AsyncIterator
from dataclasses import dataclass, field
from contextlib import asynccontextmanager

from aiogram import Dispatcher

from src.application.common.interfaces.password_encoder import PasswordEncoder
from src.presentation.telegram_admin.common.interactor_factory import Interactor, InteractorFactory
from src.main.common.gateway_factories import GatewayFactory, DatabaseGatewayFactory


__all__ = ["setup_interactor_factories"]


@dataclass(frozen=True, slots=True)
class InteractorFactoryImpl(InteractorFactory):
    
    interactor: Interactor
    factories: dict[str, GatewayFactory] = field(default_factory=dict)
    dependencies: dict[str, object] = field(default_factory=dict)

    @asynccontextmanager
    async def create_interactor(self) -> AsyncIterator[Interactor]:
        """
        Setups dependencies to interactor and returns it.
        
        Example:

        .. code-block::python
        from path_to_some_interactor_dtos import SomeInteractorDTO

        async with some_interactor_factory.create_interactor() as execute:
            await exectue(SomeInteractorDTO()) 
        """
        opened_context_managers = []
        try:
            gateways, context_managers = await self.create_gateways()
            opened_context_managers.extend(context_managers)
            self.dependencies.update(gateways)
            yield self.interactor(**self.dependencies)
        finally:
            await self.close_context_managers(opened_context_managers)
    
    async def create_gateways(self) -> tuple[dict[str, object], list[AsyncContextManager]]:
        """
        Creates gateways from gateway factories and returns them and opened
        context managers
        """
        gateways, context_managers = {}, []
        for factory_name, factory in self.factories.items():
            context_manager = factory.create_gateway()
            context_managers.append(context_manager)
            gateway = await context_manager.__aenter__()
            gateways.update({factory_name: gateway})
            
        return gateways, context_managers

    async def close_context_managers(self, context_managers: list[AsyncContextManager]) -> None:
        coros = [
            context_manager.__aexit__(None, None, None)
            for context_manager in context_managers
        ]
        await asyncio.gather(*coros)


def setup_interactor_factories(
    dispatcher: Dispatcher, interactors: list[Interactor],
    db_gateway_factory: DatabaseGatewayFactory, password_encoder: PasswordEncoder
) -> None:
    """
    Setup dependency-injected interactor factories to dispatcher.
    For Example `SomeInteractor` will be wrapped in `InteractorFactory`
    and can be used in any aiogram function like this:

    .. code-block::python
    from path_to_some_interactor import SomeInteractor
    from path_to_some_interactor_dtos import SomeInteractorDTO

    async def aiogram_function(
        message: Message,
        some_interactor_factory: InteractorFactory[SomeInteractor]
        # Note that `SomeInteractor` has become `some_interactor_factory`
    ) -> None:
        async with some_interactor_factory.create_interactor() as execute:
            await execute(SomeInteractorDTO())
    """
    
    def create_interactor_factory_name(interactor: Interactor) -> str:
        """
        Converts pascal case `interactor` name into snake case with 'interactor_factory' at the end.
        For example `SomeInteractor` will become `some_interactor_factory`
        """
        interactor_name = interactor.__name__[0].lower() + interactor.__name__[1:]
        interactor_factory_name = ""
        for letter in interactor_name:
            if letter.isupper():
                interactor_factory_name += f"_{letter.lower()}"
                continue
            interactor_factory_name += letter
        return interactor_factory_name + "_interactor_factory"

    def create_interactor_factory(interactor: Interactor) -> InteractorFactoryImpl:
        """Returns dependency-injected interactor factory"""
        factory_overrides = {"db_gateway": db_gateway_factory}
        dependency_overrides = {"password_encoder": password_encoder}
        dependencies, factories = {}, {}
        for dependency_name in interactor.__annotations__.keys():
            if dependency_name in factory_overrides:
                factories.update({dependency_name: factory_overrides[dependency_name]})
            elif dependency_name in dependency_overrides:
                dependencies.update({dependency_name: dependency_overrides[dependency_name]})
        return InteractorFactoryImpl(
            interactor=interactor, factories=factories, dependencies=dependencies
        )

    for interactor in interactors:
        name = create_interactor_factory_name(interactor)
        factory = create_interactor_factory(interactor)
        dispatcher[name] = factory