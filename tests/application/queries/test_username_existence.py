from dataclasses import dataclass, field
from datetime import datetime
from uuid import uuid4

import pytest

from src.domain.models.user.model import User
from src.domain.models.user.value_objects import UserId, Username
from src.application.queries.username_existence.query import (
    CheckUsernameExistenceQuery,
    CheckUsernameExistenceQueryResult
)
from src.application.queries.username_existence.handler import (
    CheckUsernameExistenceQueryHandler
)
from src.application.queries.username_existence.interfaces import (
    UsernameExistenceDBGateway
)


@dataclass(frozen=True, slots=True)
class FakeUsernameExistenceDBGateway(
    UsernameExistenceDBGateway
):

    users: dict[Username, User] = field(
        default_factory=dict
    )

    def check_username_existence(
        self,
        username: Username
    ) -> bool:
        return not self.users.get(username) is None


class TestCheckUsernameExistenceQuery:

    def test_valid_args(self):
        try:
            CheckUsernameExistenceQuery(
                username="johndoe"
            )
        except ValueError:
            pytest.fail()
    
    def test_invalid_args(self):
        with pytest.raises(ValueError):
            CheckUsernameExistenceQuery(
                username=""
            )
            CheckUsernameExistenceQuery(
                username=1
            )


class TestCheckUsernameExistenceQueryHandler:
    
    def test_handler_should_return_true_when_username_exists(self):
        user = User(
            id=UserId(uuid4()),
            username=Username("johndoe"),
            password="encodedpassword",
            created_at=datetime.utcnow()
        )
        users = {user.username: user}

        handler = CheckUsernameExistenceQueryHandler(
            db_gateway=FakeUsernameExistenceDBGateway(users)
        )

        query = CheckUsernameExistenceQuery(
            username=user.username.value
        )
        result = handler(query)

        assert result == CheckUsernameExistenceQueryResult(True)
    
    def test_handler_should_return_true_when_username_does_not_exist(self):
        handler = CheckUsernameExistenceQueryHandler(
            db_gateway=FakeUsernameExistenceDBGateway()
        )

        query = CheckUsernameExistenceQuery("johndoe")
        result = handler(query)

        assert result == CheckUsernameExistenceQueryResult(False)
    