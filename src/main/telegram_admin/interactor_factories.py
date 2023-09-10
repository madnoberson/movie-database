import asyncio
from typing import AsyncIterator, AsyncContextManager
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from contextlib import asynccontextmanager

from aiogram import Dispatcher

from src.application.common.interfaces.database_gateway import DatabaseGateway
from src.application.common.interfaces.password_encoder import PasswordEncoder
from src.application.interactors.user.create_user.interactor import CreateUser
from src.application.interactors.profile.create_profile.interactor import CreateProfile
from src.application.interactors.queries.user.check_email_exists.interactor import CheckEmailExists
from src.application.interactors.queries.profile.check_username_exists.interactor import CheckUsernameExists
from src.presentation.telegram_admin.common.interactor_factory import Interactor, InteractorFactory


__all__ = ["DatabaseGatewayFactory", "setup_interactor_factories"]


class GatewayFactory(ABC):

    @abstractmethod
    async def create_gateway(self) -> AsyncContextManager:
        raise NotImplementedError


class DatabaseGatewayFactory(GatewayFactory, ABC):

    @abstractmethod
    async def create_gateway(self) -> AsyncContextManager[DatabaseGateway]:
        raise NotImplementedError


@dataclass(frozen=True, slots=True)
class InteractorFactoryImpl(InteractorFactory):
    
    interactor: Interactor
    factories: dict[str, GatewayFactory] = field(default_factory=dict)
    dependencies: dict[str, object] = field(default_factory=dict)

    @asynccontextmanager
    async def create_interactor(self) -> AsyncIterator[Interactor]:
        try:
            gateways = await self.create_gateways()
            self.dependencies.update(gateways)
            yield self.interactor(**self.dependencies)
        finally:
            await self.close_gateways()
    
    async def create_gateways(self) -> dict[str, object]:
        gateways = {}
        for factory_name, factory in self.factories.items():
            context_manager = factory.create_gateway()
            gateway = await context_manager.__aenter__()
            gateways.update({factory_name: gateway})
            self.factories.update({factory_name: context_manager})
        
        return gateways

    async def close_gateways(self) -> None:
        coros = [
            context_manager.__aexit__(None, None, None)
            for context_manager in self.factories.values()
        ]
        await asyncio.gather(*coros)
        

def create_interactor_factory(
    interactor: Interactor, db_gateway_factory: DatabaseGatewayFactory,
    password_encoder: PasswordEncoder
) -> InteractorFactoryImpl:
    dependencies_override = {"password_encoder": password_encoder}
    factories_override = {"db_gateway": db_gateway_factory}

    dependencies = {}
    factories = {}
    for dependency_name in interactor.__annotations__.keys():
        if dependency_name in factories_override:
            factories.update({dependency_name: factories_override[dependency_name]})
        elif dependency_name in dependencies_override:
            dependencies.update({dependency_name: dependencies_override[dependency_name]})
    
    return InteractorFactoryImpl(interactor=interactor, factories=factories, dependencies=dependencies)


def setup_interactor_factories(
    dispatcher: Dispatcher, db_gateway_factory: DatabaseGatewayFactory,
    password_encoder: PasswordEncoder
) -> None:
    interactors = {
        "create_user": CreateUser, "create_profile": CreateProfile,
        "check_email_exists": CheckEmailExists, "check_username_exists": CheckUsernameExists
    }
    for interactor_factory_name, interactor in interactors.items():
        dispatcher[interactor_factory_name] = create_interactor_factory(
            interactor=interactor, db_gateway_factory=db_gateway_factory,
            password_encoder=password_encoder
        )