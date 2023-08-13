from dataclasses import dataclass
from datetime import datetime
from logging import getLogger
from uuid import uuid4

from src.domain.user import User
from src.application.common import utils
from . import dto
from . import errors
from . import interfaces


logger = getLogger("CreateUser")


@dataclass(frozen=True, slots=True)
class CreateUser:
    """
    ### Raises:
        * `UserAlreadyExistsError` if user already exists
        * `UnknownError` if unexpected error occured
    """

    db_gateway: interfaces.DatabaseGateway
    password_encoder: interfaces.PasswordEncoder

    @utils.handle_unexpected_exceptions(logger, errors.UserAlreadyExistsError)
    async def __call__(self, data: dto.CreateUserDTO) -> dto.CreateUserResultDTO:
        # 1.Ensure user doesn't exist
        user_exists = await self.db_gateway.ensure_user_exists(
            username=data.username
        )
        if user_exists:
            raise errors.UserAlreadyExistsError()
        
        # 2.Create user
        encoded_password = self.password_encoder.encode(
            password=data.password
        )
        user = User.create(
            user_id=uuid4(),
            username=data.username,
            encoded_password=encoded_password,
            created_at=datetime.utcnow()
        )

        # 3.Save user
        await self.db_gateway.save_user(user)
        await self.db_gateway.commit()

        return dto.CreateUserResultDTO(user_id=user.id)