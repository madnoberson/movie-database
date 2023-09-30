from dataclasses import dataclass
from datetime import datetime
from uuid import uuid4

from src.domain.user import User
from . import dto
from . import exceptions
from . import interfaces


@dataclass(frozen=True, slots=True)
class Register:

    dbw_gateway: interfaces.DatabaseWritingGateway
    password_encoder: interfaces.PasswordEncoder

    async def __call__(self, data: dto.RegisterDTO) -> dto.RegisterResultDTO:
        # 1.Ensure user doesn't exist
        user_exists = await self.dbw_gateway.check_user_exists(
            username=data.username
        )
        if user_exists:
            raise exceptions.UserAlreadyExistsError()
        
        # 2.Create user
        user = User.create(
            user_id=uuid4(), username=data.username, created_at=datetime.utcnow(),
            encoded_password=await self.password_encoder.encode(data.password)
        )

        # 3.Save user
        await self.dbw_gateway.save_user(user)
        await self.dbw_gateway.commit()

        return dto.RegisterResultDTO(user_id=user.id)