import asyncio
from typing import AsyncIterator
from dataclasses import dataclass, field
from contextlib import asynccontextmanager

from aiogram import Dispatcher

from src.application.common.interfaces.password_encoder import PasswordEncoder
from src.application.interactors.user.create_user.interactor import CreateUser
from src.application.interactors.profile.create_profile.interactor import CreateProfile
from src.application.interactors.queries.user.check_email_exists.interactor import CheckEmailExists
from src.application.interactors.queries.profile.check_username_exists.interactor import CheckUsernameExists
from src.presentation.telegram_admin.common.interactor_factory import Interactor, InteractorFactory
from src.main.common.gateway_factories import GatewayFactory, DatabaseGatewayFactory


__all__ = ["DatabaseGatewayFactory", "setup_interactor_factories"]


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
        async with interactor_factory.create_interactor() as execute:
            await exectue(InteractorDTO()) 
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
    dispatcher: Dispatcher, db_gateway_factory: DatabaseGatewayFactory,
    password_encoder: PasswordEncoder
) -> None:
    factory_overrides = {"db_gateway": db_gateway_factory}
    dependency_overrides = {"password_encoder": password_encoder}
    
    def create_interactor_factory(interactor: Interactor) -> InteractorFactoryImpl:
        """Returns dependency-injected interactor factory"""
        dependencies, factories = {}, {}
        for dependency_name in interactor.__annotations__.keys():
            if dependency_name in factory_overrides:
                factories.update({dependency_name: factory_overrides[dependency_name]})
            elif dependency_name in dependency_overrides:
                dependencies.update({dependency_name: dependency_overrides[dependency_name]})
        return InteractorFactoryImpl(
            interactor=interactor, factories=factories, dependencies=dependencies
        )

    interactors = {
        "create_user": CreateUser, "create_profile": CreateProfile,
        "check_email_exists": CheckEmailExists, "check_username_exists": CheckUsernameExists
    }
    for interactor_factory_name, interactor in interactors.items():
        dispatcher[interactor_factory_name] = create_interactor_factory(interactor)