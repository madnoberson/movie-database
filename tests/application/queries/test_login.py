from dataclasses import dataclass, field
from datetime import datetime
from uuid import uuid4

import pytest

from src.application.common.result import Result
from src.domain.models.user.model import User
from src.domain.models.user.value_objects import (
    UserId,
    Username
)
from src.application.queries.login.query import (
    LoginQuery,
    LoginQueryResult
)
from src.application.queries.login.handler import (
    LoginQueryHandler
)
from src.application.queries.login.interfaces import (
    LoginQueryDBGateway
)
from src.application.queries.login.errors import (
    UsernameDoesNotExistError,
    PasswordIsIncorrectError
)
from tests.application.mocks.password_encoder import (
    FakePasswordEncoder
)


@dataclass(frozen=True, slots=True)
class FakeLoginQueryDBGateway(LoginQueryDBGateway):
    
    users: dict[Username, User] = field(default_factory=dict)

    def get_user_by_username(
        self,
        username: Username
    ) -> User | None:
        return self.users.get(username)


class TestLoginQuery:

    def test_valid_args(self):
        try:
            LoginQuery(
                username="johndoe",
                password="password"
            )
        except ValueError:
            pytest.fail()
    
    def test_invalid_args(self):
        with pytest.raises(ValueError):
            LoginQuery(
                username="",
                password="password"
            )
            LoginQuery(
                username=1,
                password="password"
            )
            LoginQuery(
                username="johndoe",
                password="short"
            )
            LoginQuery(
                username="johnoe",
                password=1
            )
            

class TestLoginQueryHandler:

    def test_handler_should_return_user_id(self):
        user = User(
            id=UserId(uuid4()),
            username=Username("johndoe"),
            password="encodedpassword",
            created_at=datetime.utcnow()
        )
        users = {user.username: user}

        handler = LoginQueryHandler(
            db_gateway=FakeLoginQueryDBGateway(users),
            password_encoder=FakePasswordEncoder()
        )

        query = LoginQuery(
            username=user.username.value,
            password="password"
        )
        result: Result = handler(query)

        assert result.error == None
        assert result.value.user_id == user.id.value
    
    def test_handler_should_return_error_when_username_does_not_exist(self):
        handler = LoginQueryHandler(
            db_gateway=FakeLoginQueryDBGateway(),
            password_encoder=FakePasswordEncoder()
        )

        username = "johndoe"
        query = LoginQuery(
            username=username,
            password="password"
        )
        result: Result = handler(query)

        assert result.error == UsernameDoesNotExistError(username)
        assert result.value == None
    
    def test_handler_should_return_error_when_password_is_incorrect(self):
        user = User(
            id=UserId(uuid4()),
            username=Username("johndoe"),
            password="encodedpassword",
            created_at=datetime.utcnow()
        )
        users = {user.username: user}

        handler = LoginQueryHandler(
            db_gateway=FakeLoginQueryDBGateway(users),
            password_encoder=FakePasswordEncoder()
        )

        query = LoginQuery(
            username=user.username.value,
            password="incorrctpassword"
        )
        result: Result = handler(query)

        assert result.error == PasswordIsIncorrectError()
        assert result.value == None