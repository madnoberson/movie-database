from dataclasses import dataclass

from src.presentation.interactor import Interactor
from src.application.common.database_interfaces.gateway import (
    DatabaseGateway
)
from src.application.common.passoword_encoder import (
    PasswordEncoder
)
from src.application.commands.register.handler import (
    RegisterCommandHandler
)
from src.application.commands.register.command import (
    RegisterCommand,
    RegisterCommandResult
)
from src.application.queries.login.handler import (
    LoginQueryHandler
)
from src.application.queries.login.query import (
    LoginQuery,
    LoginQueryResult
)


@dataclass(frozen=True, slots=True)
class IoC(Interactor):

    db_gateway: DatabaseGateway
    password_encoder: PasswordEncoder

    def handle_register_command(
        self,
        command: RegisterCommand
    ) -> RegisterCommandResult:
        handler = RegisterCommandHandler(
            db_gateway=self.db_gateway,
            password_encoder=self.password_encoder
        )
        return handler(command)
    
    def handle_login_query(
        self,
        query: LoginQuery
    ) -> LoginQueryResult:
        handler = LoginQueryHandler(
            db_gateway=self.db_gateway,
            password_encoder=self.password_encoder
        )
        return handler(query)
    