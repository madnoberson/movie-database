from dataclasses import dataclass
from datetime import datetime
from uuid import uuid4

from src.domain.user import User
from . import dto
from . import exceptions
from . import interfaces


@dataclass(frozen=True, slots=True)
class CreateUser:

    db_gateway: interfaces.DatabaseGateway
    password_encoder: interfaces.PasswordEncoder

    async def __call__(self, data: dto.CreateUserDTO) -> dto.CreateUserResultDTO:
        # 1.Ensure user doesn't exist
        user_exists = await self.db_gateway.ensure_user_does_not_exist(
            email=data.email
        )
        if user_exists:
            raise exceptions.UserAlreadyExistsError()
        
        # 2.Create user
        encoded_password = await self.password_encoder.encode(
            plain_password=data.password
        )
        user = User.create(
            user_id=uuid4(), email=data.email,
            encoded_password=encoded_password, created_at=datetime.utcnow()
        )

        # 3.Save user
        await self.db_gateway.save_user(user)
        await self.db_gateway.commit()

        return dto.CreateUserResultDTO(user_id=user.id)