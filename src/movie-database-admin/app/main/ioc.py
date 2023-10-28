from contextlib import asynccontextmanager
from typing import AsyncIterator

from app.domain.services.access import AccessService
from app.application.common.interfaces.identity_provider import IdentityProvider
from app.application.commands.superuser.create_superuser import CreateSuperuser
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