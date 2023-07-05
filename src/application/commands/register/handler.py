from dataclasses import dataclass
from datetime import datetime
from uuid import uuid4

from src.domain.models.user.model import User
from src.domain.models.user.value_objects import UserId, Username
from src.application.common.interfaces.passoword_encoder import PasswordEncoder
from .command import RegisterCommand, RegisterCommandResult
from .interfaces import RegisterCommandDBGateway
from .errors import UsernameAlreadyExistsError


@dataclass(frozen=True, slots=True)
class RegisterCommandHandler:

    db_gateway: RegisterCommandDBGateway
    password_encoder: PasswordEncoder

    def __call__(self, command: RegisterCommand) -> RegisterCommandResult:
        username = Username(command.username)
        user = self.db_gateway.get_user_by_username(
            username=username
        )
        if user is not None:
            raise UsernameAlreadyExistsError(username.value)
        
        user_id = UserId(uuid4())
        encoded_password = self.password_encoder.encode(
            password=command.password
        )
        user = User.create(
            user_id=user_id,
            username=username,
            password=encoded_password,
            created_at=datetime.utcnow()
        )

        self.db_gateway.save_user(user)
        self.db_gateway.commit()

        return RegisterCommandResult(user_id.value)
        
