from contextlib import asynccontextmanager
from typing import AsyncIterator

from app.application.commands.registration.register import Register
from app.application.common.interfaces.identity_provider import IdentityProvider
from app.application.queries.authentication.login import Login
from app.application.queries.user.get_current_user import GetCurrentUser
from app.infrastructure.database.factories import AsyncpgFactoriesManager
from app.infrastructure.uow import UnitOfWorkImpl
from app.presentation.handler_factory import HandlerFactory


class IoC(HandlerFactory):

    def __init__(self, factories_manager: AsyncpgFactoriesManager) -> None:
        self.factories_manager = factories_manager

    @asynccontextmanager
    async def register(self) -> AsyncIterator[Register]:
        async with self.factories_manager.build_repository_factory() as factory:
            yield Register(
                user_repo=factory.build_user_repo(),
                uow=UnitOfWorkImpl(await factory.build_uow())
            )

    @asynccontextmanager
    async def login(self) -> AsyncIterator[Login]:
        async with self.factories_manager.build_reader_factory() as factory:
            yield Login(auth_reader=factory.build_authentication_reader())
    
    @asynccontextmanager
    async def get_current_user(
        self, identity_provider: IdentityProvider
    ) -> AsyncIterator[GetCurrentUser]:
        async with self.factories_manager.build_reader_factory() as factory:
            yield GetCurrentUser(
                user_reader=factory.build_user_reader(),
                identity_provider=identity_provider
            )
