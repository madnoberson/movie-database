from abc import ABC, abstractmethod

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
from src.application.queries.username_existence.query import (
    CheckUsernameExistenceQuery
)
from src.application.queries.username_existence.handler import (
    QueryHandlerResult as CheckUsernameExistenceQueryHandlerResult
)


class ApiInteractor(ABC):
    
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
    
    @abstractmethod
    def handle_check_username_existence_query(
        self,
        query: CheckUsernameExistenceQuery
    ) -> CheckUsernameExistenceQueryHandlerResult:
        raise NotImplementedError

