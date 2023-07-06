from dataclasses import dataclass, field
from datetime import datetime
from uuid import uuid4, UUID

import pytest

from src.domain.models.user.model import User
from src.domain.models.user.value_objects import UserId, Username
from src.application.commands.register.command import RegisterCommand, RegisterCommandResult
from src.application.commands.register.handler import RegisterCommandHandler
from src.application.commands.register.interfaces import RegisterCommandDBGateway
from src.application.commands.register.errors import UsernameAlreadyExistsError
from tests.application.mocks.password_encoder import FakePasswordEncoder


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

    def test_valid_args(self):
        try:
            RegisterCommand(
                username="johndoe",
                password="password"
            )
        except ValueError:
            pytest.fail()
    
    def test_invalid_args(self):
        with pytest.raises(ValueError):
            RegisterCommand(
                username="",
                password="password"
            )
            RegisterCommand(
                username=1,
                password="password"
            )
            RegisterCommand(
                username="johndoe",
                password="short"
            )
            RegisterCommand(
                username="johndoe",
                password=1
            )


class TestRegisterCommandHandler:
    
    def test_handler_should_return_normal_result(self):
        handler = RegisterCommandHandler(
            db_gateway=FakeRegisterCommandDBGateway(),
            password_encoder=FakePasswordEncoder()
        )

        username = "johndoe"
        command = RegisterCommand(
            username=username,
            password="secretpassword"
        )

        try:
            result = handler(command)
        except UsernameAlreadyExistsError:
            pytest.fail()

        assert isinstance(result, RegisterCommandResult)
        assert isinstance(result.user_id, UUID)

    def test_handler_should_raise_error_when_username_already_exists(self):
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

        with pytest.raises(UsernameAlreadyExistsError) as e:
            handler(command)

        assert e.value == UsernameAlreadyExistsError(user.username.value)

        