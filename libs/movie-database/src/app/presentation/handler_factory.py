from abc import ABC, abstractmethod
from typing import AsyncContextManager

from app.application.common.interfaces.identity_provider import IdentityProvider
from app.application.commands.registration.register import Register
from app.application.commands.user.change_username import ChangeUsername
from app.application.commands.user.change_password import ChangePassword
from app.application.commands.movie_rating.rate_movie import RateMovie
from app.application.commands.movie_rating.rerate_movie import RerateMovie
from app.application.commands.movie_rating.unrate_movie import UnrateMovie
from app.application.commands.user.ensure_username_change import EnsureUsernameChange
from app.application.commands.movie.ensure_movie import EnsureMovie
from app.application.queries.auth.login import Login
from app.application.queries.user.get_current_user import GetCurrentUser


class HandlerFactory(ABC):

    @abstractmethod
    async def register(self) -> AsyncContextManager[Register]:
        raise NotImplementedError
    
    @abstractmethod
    async def change_username(
        self, identity_provider: IdentityProvider
    ) -> AsyncContextManager[ChangeUsername]:
        raise NotImplementedError
    
    @abstractmethod
    async def change_password(
        self, identity_provider: IdentityProvider
    ) -> AsyncContextManager[ChangePassword]:
        raise NotImplementedError
    
    @abstractmethod
    async def rate_movie(
        self, identity_provider: IdentityProvider
    ) -> AsyncContextManager[RateMovie]:
        raise NotImplementedError
    
    @abstractmethod
    async def rerate_movie(
        self, identity_provider: IdentityProvider
    ) -> AsyncContextManager[RerateMovie]:
        raise NotImplementedError

    @abstractmethod
    async def unrate_movie(
        self, identity_provider: IdentityProvider
    ) -> AsyncContextManager[UnrateMovie]:
        raise NotImplementedError
    
    @abstractmethod
    async def ensure_username_change(
        self
    ) -> AsyncContextManager[EnsureUsernameChange]:
        raise NotImplementedError
    
    @abstractmethod
    async def ensure_movie(self) -> AsyncContextManager[EnsureMovie]:
        raise NotImplementedError

    @abstractmethod
    async def login(self) -> AsyncContextManager[Login]:
        raise NotImplementedError

    @abstractmethod
    async def get_current_user(
        self, identity_provider: IdentityProvider
    ) -> AsyncContextManager[GetCurrentUser]:
        raise NotImplementedError