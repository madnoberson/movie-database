from dataclasses import dataclass, field
from datetime import datetime
from uuid import uuid4, UUID

from src.application.common.result import Result
from src.domain.models.user.model import User
from src.domain.models.user.value_objects import (
    UserId,
    Username
)
from src.application.commands.register.command import (
    RegisterCommand,
    RegisterCommandResult
)
from src.application.commands.register.handler import (
    RegisterCommandHandler
)
from src.application.commands.register.interfaces import (
    RegisterCommandDBGateway
)
from src.application.commands.register.errors import (
    UsernameAlreadyExistsError
)
from tests.application.mocks.password_encoder import (
    FakePasswordEncoder
)


@dataclass(frozen=True, slots=True)
class FakeRegisterCommandDBGateway(
    RegisterCommandDBGateway
):

    users: dict[Username, User] = field(
        default_factory=dict
    )

    def save_user(self, user: User) -> None:
        self.users[user.username] = user
    
    def get_user_by_username(
        self,
        username: Username
    ) -> User | None:
        return self.users.get(username)

    def commit(self) -> None:
        ...
    
    def rollback(self) -> None:
        ...
    

class TestRegisterCommand:
    
    def test_handler_should_return_user_id(self):
        handler = RegisterCommandHandler(
            db_gateway=FakeRegisterCommandDBGateway(),
            password_encoder=FakePasswordEncoder()
        )

        username = "johndoe"
        command = RegisterCommand(
            username=username,
            password="secretpassword"
        )
        result: Result = handler(command)

        assert result.error == None
        assert isinstance(result.value, RegisterCommandResult)
        assert isinstance(result.value.user_id, UUID)

    def test_handler_should_return_error_when_username_already_exists(self):
        user = User(
            id=UserId(uuid4()),
            username=Username("johndoe"),
            password="secretpassword",
            created_at=datetime.utcnow()
        )
        users = {user.username: user}

        handler = RegisterCommandHandler(
            db_gateway=FakeRegisterCommandDBGateway(users),
            password_encoder=FakePasswordEncoder()
        )

        command = RegisterCommand(
            username=user.username.value,
            password="secretpassword"
        )
        result: Result = handler(command)

        assert result.value == None
        assert result.error == UsernameAlreadyExistsError(user.username.value)

        