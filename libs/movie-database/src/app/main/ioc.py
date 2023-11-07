from contextlib import asynccontextmanager
from typing import AsyncIterator

from app.domain.services.movie_rating import MovieRatingService
from app.application.common.interfaces.identity_provider import IdentityProvider
from app.application.commands.registration.register import Register
from app.application.commands.user.change_username import ChangeUsername
from app.application.commands.user.change_password import ChangePassword
from app.application.commands.movie_rating.rate_movie import RateMovie
from app.application.commands.movie_rating.rerate_movie import RerateMovie
from app.application.commands.user.ensure_username_change import EnsureUsernameChange
from app.application.commands.movie.ensure_movie import EnsureMovie
from app.application.queries.auth.login import Login
from app.application.queries.user.get_current_user import GetCurrentUser
from app.infrastructure.database.factory import DatabaseFactoryManager
from app.infrastructure.message_broker.factory import EventBusFactory
from app.infrastructure.uow import UnitOfWorkImpl
from app.presentation.handler_factory import HandlerFactory


class IoC(HandlerFactory):

    def __init__(
        self,
        db_factory_manager: DatabaseFactoryManager,
        event_bus_factory: EventBusFactory,
        movie_rating_service: MovieRatingService
    ) -> None:
        self.db_factory_manager = db_factory_manager
        self.event_bus_factory = event_bus_factory
        self.movie_rating_service = movie_rating_service

    @asynccontextmanager
    async def register(self) -> AsyncIterator[Register]:
        async with (
            self.db_factory_manager.build_repo_factory() as repo_factory,
            self.event_bus_factory.build_event_bus() as event_bus
        ):
            yield Register(
                user_repo=repo_factory.build_user_repo(),
                event_bus=event_bus,
                uow=UnitOfWorkImpl(await repo_factory.build_uow(), event_bus.build_uow())
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
                identity_provider=identity_provider,
                uow=UnitOfWorkImpl(await repo_factory.build_uow(), event_bus.build_uow())
            )
    
    @asynccontextmanager
    async def change_password(
        self, identity_provider: IdentityProvider
    ) -> AsyncIterator[ChangePassword]:
        async with self.db_factory_manager.build_repo_factory() as repo_factory:
            yield ChangePassword(
                user_repo=repo_factory.build_user_repo(),
                identity_provider=identity_provider,
                uow=UnitOfWorkImpl(await repo_factory.build_uow())
            )
    
    @asynccontextmanager
    async def rate_movie(
        self, identity_provider: IdentityProvider
    ) -> AsyncIterator[RateMovie]:
        async with (
            self.db_factory_manager.build_repo_factory() as repo_factory,
            self.event_bus_factory.build_event_bus() as event_bus
        ):
            yield RateMovie(
                movie_rating_repo=repo_factory.build_movie_rating_repo(),
                movie_repo=repo_factory.build_movie_repo(),
                user_repo=repo_factory.build_user_repo(),
                movies_rating_policy_repo=repo_factory.build_movies_rating_policy_repo(),
                event_bus=event_bus,
                identity_provider=identity_provider,
                movie_rating_service=self.movie_rating_service,
                uow=UnitOfWorkImpl(await repo_factory.build_uow(), event_bus.build_uow())
            )
    
    @asynccontextmanager
    async def rerate_movie(
        self, identity_provider: IdentityProvider
    ) -> AsyncIterator[RerateMovie]:
        async with (
            self.db_factory_manager.build_repo_factory() as repo_factory,
            self.event_bus_factory.build_event_bus() as event_bus
        ):
            yield RerateMovie(
                movie_rating_repo=repo_factory.build_movie_rating_repo(),
                movie_repo=repo_factory.build_movie_repo(),
                user_repo=repo_factory.build_user_repo(),
                movies_rating_policy_repo=repo_factory.build_movies_rating_policy_repo(),
                event_bus=event_bus,
                identity_provider=identity_provider,
                movie_rating_service=self.movie_rating_service,
                uow=UnitOfWorkImpl(await repo_factory.build_uow(), event_bus.build_uow())
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
    async def ensure_movie(self) -> AsyncIterator[EnsureMovie]:
        async with self.db_factory_manager.build_repo_factory() as repo_factory:
            yield EnsureMovie(
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
