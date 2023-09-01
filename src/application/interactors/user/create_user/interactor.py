import asyncio
from logging import getLogger
from dataclasses import dataclass
from datetime import datetime
from uuid import uuid4

from src.domain.user import User
from src.application.common import utils
from . import dto
from . import errors
from . import interfaces


logger = getLogger("CreateUser")


@dataclass(frozen=True, slots=True)
class CreateUser:

    db_gateway: interfaces.DatabaseGateway
    cb_gateway: interfaces.CachebaseGateway
    tq_gateway: interfaces.TaskQueueGateway
    password_encoder: interfaces.PasswordEncoder

    @utils.handle_unexpected_exceptions(
        logger, errors.EmailAlreadyExistsError, errors.UserNotConfirmedError
    )
    async def __call__(self, data: dto.CreateUserDTO) -> dto.CreateUserResultDTO:
        # 1.Ensure user doesn't exist
        await self.ensure_user_does_not_exist(email=data.email)

        # 2.Create user
        encoded_password = await self.password_encoder.encode(
            plain_password=data.password
        )
        user = User.create(
            user_id=uuid4(), email=data.email, username=data.email,
            encoded_password=encoded_password, created_at=datetime.utcnow()
        )

        # 3.Save user and enqueue `send_confirmation_email` task
        await asyncio.gather(
            self.db_gateway.save_user(user), self.cb_gateway.save_user(user),
            self.tq_gateway.enqueue_send_confirmation_task(email=data.email)
        )
        await asyncio.gather(
            self.db_gateway.commit(), self.cb_gateway.commit(), self.tq_gateway.commit()
        )

        return dto.CreateUserResultDTO(user_id=user.id)
    
    async def ensure_user_does_not_exist(self, email: str) -> None:
        # 1.Get user
        user = await self.get_user(email=email)
        if user is None: return

        if not user.is_confirmed:
            raise errors.UserNotConfirmedError()
        
        raise errors.EmailAlreadyExistsError()
    
    async def get_user(self, email: str) -> User | None:
        # 1.Get user from cachebase
        user = await self.cb_gateway.get_user(email=email)
        if user is not None: return user

        # 2.Get user from database
        user = await self.db_gateway.get_user(email=email)
        if user is not None:
            await self.cb_gateway.save_user(user)
        
        return user
