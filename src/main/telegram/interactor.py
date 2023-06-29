from dataclasses import dataclass

from src.presentation.telegram.interactor import TelegramInteractor
from src.application.common.database_interfaces.gateway import (
    DatabaseGateway
)
from src.application.common.passoword_encoder import (
    PasswordEncoder
)
from src.application.commands.register.command import (
    RegisterCommand
)
from src.application.commands.register.handler import (
    RegisterCommandHandler,
    CommandHandlerResult as RegisterCommandHandlerResult
)
from src.application.queries.username_existence.query import (
    CheckUsernameExistenceQuery
)
from src.application.queries.username_existence.handler import (
    CheckUsernameExistenceQueryHandler,
    QueryHandlerResult as CheckUsernameExistenceQueryHandlerResult
)


@dataclass(frozen=True, slots=True)
class TelegramInteractorImpl(TelegramInteractor):

    db_gateway: DatabaseGateway
    password_encoder: PasswordEncoder

    def handle_register_command(
        self,
        command: RegisterCommand
    ) -> RegisterCommandHandlerResult:
        handler = RegisterCommandHandler(
            db_gateway=self.db_gateway,
            password_encoder=self.password_encoder
        )
        return handler(command)

    def handle_check_username_existence_query(
        self,
        query: CheckUsernameExistenceQuery
    ) -> CheckUsernameExistenceQueryHandlerResult:
        hanlder = CheckUsernameExistenceQueryHandler(
            db_gateway=self.db_gateway
        )
        return hanlder(query)
    