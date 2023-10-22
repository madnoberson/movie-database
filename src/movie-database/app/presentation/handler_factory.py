from abc import ABC, abstractmethod
from typing import AsyncContextManager

from app.application.common.interfaces.identity_provider import IdentityProvider
from app.application.commands.registration.register import Register
from app.application.commands.adding_task.create_task import CreateAddingTask
from app.application.commands.movie.create_movie import CreateMovie
from app.application.queries.auth.login import Login
from app.application.queries.user.get_current_user import GetCurrentUser


class HandlerFactory(ABC):

    @abstractmethod
    async def register(self) -> AsyncContextManager[Register]:
        raise NotImplementedError
    
    @abstractmethod
    async def create_adding_task(
        self, identity_provider: IdentityProvider
    ) -> AsyncContextManager[CreateAddingTask]:
        raise NotImplementedError
    
    @abstractmethod
    async def create_movie(self) -> AsyncContextManager[CreateMovie]:
        raise NotImplementedError

    @abstractmethod
    async def login(self) -> AsyncContextManager[Login]:
        raise NotImplementedError

    @abstractmethod
    async def get_current_user(
        self, identity_provider: IdentityProvider
    ) -> AsyncContextManager[GetCurrentUser]:
        raise NotImplementedError