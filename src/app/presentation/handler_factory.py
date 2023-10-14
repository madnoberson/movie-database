from abc import ABC, abstractmethod
from typing import AsyncContextManager

from app.application.common.interfaces.identity_provider import IdentityProvider
from app.application.commands.registration.register import Register
from app.application.queries.authentication.login import Login
from app.application.queries.user.get_current_user import GetCurrentUser


class HandlerFactory(ABC):

    @abstractmethod
    async def register(self) -> AsyncContextManager[Register]:
        raise NotImplementedError
    
    @abstractmethod
    async def login(self) -> AsyncContextManager[Login]:
        raise NotImplementedError
    
    @abstractmethod
    async def get_current_user(
        self, identity_provider: IdentityProvider
    ) -> AsyncContextManager[GetCurrentUser]:
        raise NotImplementedError