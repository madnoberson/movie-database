from contextlib import asynccontextmanager
from typing import AsyncIterator

from app.domain.services.access import AccessService
from app.application.common.interfaces.identity_provider import IdentityProvider
from app.application.commands.superuser.create_superuser import CreateSuperuser
from app.application.commands.user.change_username import ChangeUsername
from app.application.commands.user.ensure_user import EnsureUser
from app.application.commands.user.ensure_username_change import EnsureUsernameChange
from app.application.queries.auth.login import Login
from app.infrastructure.database.factory import DatabaseFactoryManager
from app.infrastructure.message_broker.factory import EventBusFactory
from app.infrastructure.uow import UnitOfWorkImpl
from app.presentation.handler_factory import HandlerFactory


class IoC(HandlerFactory):

    def __init__(
        self,
        db_factory_manager: DatabaseFactoryManager,
        event_bus_factory: EventBusFactory,
        access_service: AccessService
    ) -> None:
        self.db_factory_manager = db_factory_manager
        self.event_bus_factory = event_bus_factory
        self.access_service = access_service    

    @asynccontextmanager
    async def create_superuser(
        self, identity_provider: IdentityProvider
    ) -> AsyncIterator[CreateSuperuser]:
        async with self.db_factory_manager.build_repo_factory() as repo_factory:
            yield CreateSuperuser(
                superuser_repo=repo_factory.build_superuser_repo(),
                identity_provider=identity_provider,
                access_service=self.access_service,
                uow=UnitOfWorkImpl(await repo_factory.build_uow())
            )
    
    @asynccontextmanager
    async def change_username(
        self, identity_provider: IdentityProvider
    ) -> AsyncIterator[ChangeUsername]:
        async with (
            self.db_factory_manager.build_repo_factory() as repo_factory,
            self.event_bus_factory.build_event_bus() as event_bus
        ):
            yield ChangeUsername(
                user_repo=repo_factory.build_user_repo(),
                event_bus=event_bus,
                access_service=self.access_service,
                identity_provider=identity_provider,
                uow=UnitOfWorkImpl(await repo_factory.build_uow(), event_bus.build_uow())
            )

    @asynccontextmanager
    async def ensure_user(self) -> AsyncIterator[EnsureUser]:
        async with self.db_factory_manager.build_repo_factory() as repo_factory:
            yield EnsureUser(
                user_repo=repo_factory.build_user_repo(),
                uow=UnitOfWorkImpl(await repo_factory.build_uow())
            )
    
    @asynccontextmanager
    async def ensure_username_change(
        self
    ) -> AsyncIterator[EnsureUsernameChange]:
        async with self.db_factory_manager.build_repo_factory() as repo_factory:
            yield EnsureUsernameChange(
                user_repo=repo_factory.build_user_repo(),
                uow=UnitOfWorkImpl(await repo_factory.build_uow())
            )

    @asynccontextmanager
    async def login(self) -> AsyncIterator[Login]:
        async with self.db_factory_manager.build_reader_factory() as reader_factory:
            yield Login(auth_reader=reader_factory.build_auth_reader())