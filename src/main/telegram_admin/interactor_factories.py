import asyncio
from typing import AsyncIterator
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
        try:
            gateways = await self.open_gateways()
            self.dependencies.update(gateways)
            yield self.interactor(**self.dependencies)
        finally:
            await self.close_gateways()
    
    async def open_gateways(self) -> dict[str, object]:
        """Creates gateways from gateway factories and returns them"""
        gateways = {}
        for factory_name, factory in self.factories.items():
            context_manager = factory.create_gateway()
            gateway = await context_manager.__aenter__()
            gateways.update({factory_name: gateway})
            self.factories.update({factory_name: context_manager})
            
        return gateways

    async def close_gateways(self) -> None:
        """Closes opened gateways"""
        coros = [
            context_manager.__aexit__(None, None, None)
            for context_manager in self.factories.values()
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
                interactor_factory_name += f"_{letter}"
                continue
            interactor_factory_name += letter
        return interactor_name + "_interactor_factory"

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