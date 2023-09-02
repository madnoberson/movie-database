import asyncio
from logging import getLogger
from dataclasses import dataclass
from datetime import datetime

from src.application.common import utils
from src.application.common import mixins
from . import dto
from . import errors
from . import interfaces


logger = getLogger("UpdateEmail")


@dataclass(frozen=True, slots=True)
class UpdateEmail(mixins.SupportsGetAndCacheUser):

    db_gateway: interfaces.DatabaseGateway
    cb_gateway: interfaces.CachebaseGateway
    tq_gateway: interfaces.TaskQueueGateway

    @utils.handle_unexpected_exceptions(
        logger, errors.UserDoesNotExistError, errors.UserNotActiveError,
        errors.EmailIsSameAsPreviousError
    )
    async def __call__(self, data: dto.UpdateEmailDTO) -> None:
        # 1.Get user
        user = await self.get_and_cache_user(
            db_gateway=self.db_gateway, cb_gateway=self.cb_gateway,
            user_id=data.user_id
        )
        if user is None:
            raise errors.UserDoesNotExistError()
        
        # 2.Ensure user is active
        if not user.is_active:
            raise errors.UserNotActiveError()
        
        # 3.Update email
        user.update_email(
            email=data.email, updated_at=datetime.utcnow()
        )

        # 4.Save changes and enqueue `send_update_email_confirmation_email` task
        await asyncio.gather(
            self.db_gateway.update_user(user), self.cb_gateway.update_user(user),
            self.tq_gateway.enqueue_send_update_email_confirmation_email_task(email=data.email)
        )
        await asyncio.gather(
            self.db_gateway.commit(), self.cb_gateway.commit(), self.tq_gateway.commit()
        )