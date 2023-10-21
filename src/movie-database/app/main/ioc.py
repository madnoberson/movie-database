from contextlib import asynccontextmanager
from typing import AsyncIterator

from app.application.common.interfaces.identity_provider import IdentityProvider
from app.application.commands.registration.register import Register
from app.application.commands.movie.create_movie import CreateMovie
from app.application.queries.authentication.login import Login
from app.application.queries.user.get_current_user import GetCurrentUser
from app.infrastructure.database.factory import AsyncpgFactoryManager
from app.infrastructure.uow import UnitOfWorkImpl
from app.presentation.handler_factory import HandlerFactory


class IoC(HandlerFactory):

    def __init__(self, db_factory_manager: AsyncpgFactoryManager) -> None:
        self.db_factory_manager = db_factory_manager

    @asynccontextmanager
    async def register(self) -> AsyncIterator[Register]:
        async with self.db_factory_manager.build_repository_factory() as factory:
            yield Register(
                user_repo=factory.build_user_repo(),
                uow=UnitOfWorkImpl(await factory.build_uow())
            )
    
    @asynccontextmanager
    async def create_movie(self) -> AsyncIterator[CreateMovie]:
        async with self.db_factory_manager.build_repository_factory() as factory:
            yield CreateMovie(
                movie_repo=factory.build_movie_repo(),
                uow=UnitOfWorkImpl(await factory.build_uow())
            )

    @asynccontextmanager
    async def login(self) -> AsyncIterator[Login]:
        async with self.db_factory_manager.build_reader_factory() as factory:
            yield Login(auth_reader=factory.build_authentication_reader())
    
    @asynccontextmanager
    async def get_current_user(
        self, identity_provider: IdentityProvider
    ) -> AsyncIterator[GetCurrentUser]:
        async with self.db_factory_manager.build_reader_factory() as factory:
            yield GetCurrentUser(
                user_reader=factory.build_user_reader(),
                identity_provider=identity_provider
            )
