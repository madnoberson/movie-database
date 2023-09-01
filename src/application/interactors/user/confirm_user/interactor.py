import asyncio
from logging import getLogger
from dataclasses import dataclass

from src.domain.user import User
from src.application.common import utils
from . import dto
from . import errors
from . import interfaces


logger = getLogger("ConfirmUser")


@dataclass(frozen=True, slots=True)
class ConfirmUser:

    db_gateway: interfaces.DatabaseGateway
    cb_gateway: interfaces.CachebaseGateway
    tq_gateway: interfaces.TaskQueueGateway

    @utils.handle_unexpected_exceptions(
        logger, errors.UserDoesNotExistError, errors.UserAlreadyConfirmedError
    )
    async def __call__(self, data: dto.ConfirmUserDTO) -> None:
        # 1.Get user
        user = await self.get_user(email=data.email)
        if user is None:
            raise errors.UserDoesNotExistError()
        
        # 2.Ensure user is not confirmed
        if user.is_confirmed:
            raise errors.UserAlreadyConfirmedError()
        
        # 3.Confirm user
        user.confirm()

        # 4.Save changes and enqueue `send_greeting_email` task
        await asyncio.gather(
            self.db_gateway.update_user(user), self.cb_gateway.update_user(user),
            self.tq_gateway.enqueue_send_greeting_email_task(user_id=user.id)
        )
        await asyncio.gather(
            self.db_gateway.commit(), self.cb_gateway.commit(), self.tq_gateway.commit()
        )
    
    async def get_user(self, email: str) -> User | None:
        # 1.Get user from cachebase
        user = await self.cb_gateway.get_user(email=email)
        if user is not None: return user

        # 2.Get user from database
        user = await self.db_gateway.get_user(email=email)
        if user is not None:
            await self.cb_gateway.save_user(user)
        
        return user