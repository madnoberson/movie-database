from typing import AsyncContextManager
from abc import ABC, abstractmethod

from app.application.common.interfaces.identity_provider import IdentityProvider
from app.application.commands.superuser.create_superuser import CreateSuperuser
from app.application.commands.superuser.change_password import ChangeSuperuserPassword
from app.application.commands.user.change_username import ChangeUsername
from app.application.commands.user.ensure_user import EnsureUser
from app.application.commands.user.ensure_username_change import EnsureUsernameChange
from app.application.queries.auth.login import Login


class HandlerFactory(ABC):

    @abstractmethod
    async def create_superuser(
        self, identity_provider: IdentityProvider
    ) -> AsyncContextManager[CreateSuperuser]:
        raise NotImplementedError
    
    @abstractmethod
    async def change_superuser_password(
        self, identity_provider: IdentityProvider
    ) -> AsyncContextManager[ChangeSuperuserPassword]:
        raise NotImplementedError

    @abstractmethod
    async def change_username(
        self, identity_provider: IdentityProvider
    ) -> AsyncContextManager[ChangeUsername]:
        raise NotImplementedError
    
    @abstractmethod
    async def ensure_user(self) -> AsyncContextManager[EnsureUser]:
        raise NotImplementedError
    
    @abstractmethod
    async def ensure_username_change(
        self
    ) -> AsyncContextManager[EnsureUsernameChange]:
        raise NotImplementedError
    
    @abstractmethod
    async def login(self) -> AsyncContextManager[Login]:
        raise NotImplementedError