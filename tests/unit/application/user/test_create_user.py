from unittest.mock import AsyncMock

import pytest

from src.application.interactors.user.create_user import dto
from src.application.interactors.user.create_user import errors
from src.application.interactors.user.create_user import interfaces
from src.application.interactors.user.create_user.interactor import CreateUser


@pytest.mark.anyio
class TestCreateUser:

    async def test_interactor_should_create_user(
        self,
        db_gateway: interfaces.DatabaseGateway,
        password_encoder: interfaces.PasswordEncoder
    ):
        db_gateway.ensure_user_exists = AsyncMock(return_value=False)
        
        data = dto.CreateUserDTO(username="username", password="password")
        create_user = CreateUser(db_gateway=db_gateway, password_encoder=password_encoder)

        await create_user(data)
    
    async def test_interactor_should_raise_error_when_user_already_exists(
        self,
        db_gateway: interfaces.DatabaseGateway,
        password_encoder: interfaces.PasswordEncoder
    ):
        db_gateway.ensure_user_exists = AsyncMock(return_value=True)
        
        data = dto.CreateUserDTO(username="username", password="password")
        create_user = CreateUser(db_gateway=db_gateway, password_encoder=password_encoder)

        with pytest.raises(errors.UserAlreadyExistsError):
            await create_user(data)