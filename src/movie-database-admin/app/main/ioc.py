from contextlib import asynccontextmanager
from typing import AsyncIterator

from app.domain.services.access import AccessService
from app.application.common.interfaces.identity_provider import IdentityProvider
from app.application.commands.superuser.create_superuser import CreateSuperuser
from app.application.commands.user.ensure_user import EnsureUser
from app.application.queries.auth.login import Login
from app.infrastructure.database.factory import DatabaseFactoryManager
from app.infrastructure.uow import UnitOfWorkImpl
from app.presentation.handler_factory import HandlerFactory


class IoC(HandlerFactory):

    def __init__(
        self,
        db_factory_manager: DatabaseFactoryManager,
        access_service: AccessService
    ) -> None:
        self.db_factory_manager = db_factory_manager
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
    async def ensure_user(self) -> AsyncIterator[EnsureUser]:
        async with self.db_factory_manager.build_repo_factory() as repo_factory:
            yield EnsureUser(
                user_repo=repo_factory.build_user_repo(),
                uow=UnitOfWorkImpl(await repo_factory.build_uow())
            )

    @asynccontextmanager
    async def login(self) -> AsyncIterator[Login]:
        async with self.db_factory_manager.build_reader_factory() as reader_factory:
            yield Login(auth_reader=reader_factory.build_auth_reader())