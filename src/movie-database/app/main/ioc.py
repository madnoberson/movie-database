from contextlib import asynccontextmanager
from typing import AsyncIterator

from app.application.common.interfaces.identity_provider import IdentityProvider
from app.application.commands.registration.register import Register
from app.application.commands.movie.create_movie import CreateMovie
from app.application.queries.auth.login import Login
from app.application.queries.user.get_current_user import GetCurrentUser
from app.infrastructure.database.factory import DatabaseFactoryManager
from app.infrastructure.uow import UnitOfWorkImpl
from app.presentation.handler_factory import HandlerFactory


class IoC(HandlerFactory):

    def __init__(self, db_factory_manager: DatabaseFactoryManager) -> None:
        self.db_factory_manager = db_factory_manager

    @asynccontextmanager
    async def register(self) -> AsyncIterator[Register]:
        async with self.db_factory_manager.build_repo_factory() as repo_factory:
            yield Register(
                user_repo=repo_factory.build_user_repo(),
                uow=UnitOfWorkImpl(await repo_factory.build_uow())
            )
    
    @asynccontextmanager
    async def create_movie(self) -> AsyncIterator[CreateMovie]:
        async with self.db_factory_manager.build_repo_factory() as repo_factory:
            yield CreateMovie(
                movie_repo=repo_factory.build_movie_repo(),
                uow=UnitOfWorkImpl(await repo_factory.build_uow())
            )

    @asynccontextmanager
    async def login(self) -> AsyncIterator[Login]:
        async with self.db_factory_manager.build_reader_factory() as reader_factory:
            yield Login(auth_reader=reader_factory.build_auth_reader())
    
    @asynccontextmanager
    async def get_current_user(
        self, identity_provider: IdentityProvider
    ) -> AsyncIterator[GetCurrentUser]:
        async with self.db_factory_manager.build_reader_factory() as reader_factory:
            yield GetCurrentUser(
                user_reader=reader_factory.build_user_reader(),
                identity_provider=identity_provider
            )
