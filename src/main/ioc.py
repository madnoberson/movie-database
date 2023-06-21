from contextlib import contextmanager
from dataclasses import dataclass

from src.presentation.interactor_factory import InteractorFactory
from src.application.common.database_intefaces.gateway import DatabaseGateway
from src.application.common.passoword_encoder import PasswordEncoder
from src.application.commands.register.handler import RegisterCommandHandler
from src.application.queries.login.handler import LoginQueryHandler


@dataclass(frozen=True, slots=True)
class IoC(InteractorFactory):

    db_gateway: DatabaseGateway
    password_encoder: PasswordEncoder

    @contextmanager
    def register(self) -> RegisterCommandHandler:
        yield RegisterCommandHandler(
            db_gateway=self.db_gateway,
            password_encoder=self.password_encoder
        )
    
    @contextmanager
    def login(self) -> LoginQueryHandler:
        yield LoginQueryHandler(
            db_gateway=self.db_gateway,
            password_encoder=self.password_encoder
        )