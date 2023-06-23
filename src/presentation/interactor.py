from abc import ABC, abstractmethod
from dataclasses import dataclass

from src.application.commands.register.command import (
    RegisterCommand
)
from src.application.commands.register.handler import (
    CommandHandlerResult as RegisterCommandHandlerResult
)
from src.application.queries.login.query import (
    LoginQuery
)
from src.application.queries.login.handler import (
    QueryHanlderResult as LoginQueryHandlerResult
)


@dataclass(frozen=True, slots=True)
class Interactor(ABC):
    
    @abstractmethod
    def handle_register_command(
        self,
        command: RegisterCommand
    ) -> RegisterCommandHandlerResult:
        raise NotImplementedError

    @abstractmethod
    def handle_login_query(
        self,
        query: LoginQuery
    ) -> LoginQueryHandlerResult:
        raise NotImplementedError

