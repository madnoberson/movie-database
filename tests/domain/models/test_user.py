from uuid import uuid4
from datetime import datetime

from src.domain.models.user.model import User
from src.domain.models.user.value_objects import (
    UserId,
    Username
)


class TestUser:

    def test_create_should_return_user(self):
        user_id = UserId(uuid4())
        username = Username("johndoe")
        password = "encodedpassword"
        created_at = datetime.utcnow()

        user = User.create(
            user_id=user_id,
            username=username,
            password=password,
            created_at=created_at
        )

        assert user.id == user_id
        assert user.username == username
        assert user.password == password
        assert user.created_at == created_at
    
    def test_constructor_should_return_user(self):
        user_id = UserId(uuid4())
        username = Username("johndoe")
        password = "encodedpassword"
        created_at = datetime.utcnow()

        user = User(
            id=user_id,
            username=username,
            password=password,
            created_at=created_at
        )

        assert user.id == user_id
        assert user.username == username
        assert user.password == password
        assert user.created_at == created_at
    
    def test_change_username_shoul_change_username(self):
        user_id = UserId(uuid4())
        username = Username("johndoe")
        password = "encodedpassword"
        created_at = datetime.utcnow()

        user = User(
            id=user_id,
            username=username,
            password=password,
            created_at=created_at
        )

        new_username = Username("janedoe")
        user.change_username(new_username)

        assert user.username == new_username
