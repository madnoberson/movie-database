import asyncio
from logging import getLogger
from dataclasses import dataclass
from datetime import datetime

from src.application.common import utils
from src.application.common import mixins
from . import dto
from . import errors
from . import interfaces


logger = getLogger("UpdateUsername")


@dataclass(frozen=True, slots=True)
class UpdateUsername(mixins.SupportsGetAndCacheUser):

    db_gateway: interfaces.DatabaseGateway
    cb_gateway: interfaces.CachebaseGateway

    @utils.handle_unexpected_exceptions(
        logger, errors.UserDoesNotExistError, errors.UserNotActiveError,
        errors.UserNotConfirmedError
    )
    async def __call__(self, data: dto.UpdateUsernameDTO) -> None:
        # 1.Get user
        user = await self.get_and_cache_user(
            db_gateway=self.db_gateway, cb_gateway=self.cb_gateway,
            user_id=data.user_id
        )
        if user is None:
            raise errors.UserDoesNotExistError()
        
        # 2.Ensure user is confirmed
        if not user.is_confirmed:
            raise errors.UserNotConfirmedError()
        
        # 3.Ensure user is active
        if not user.is_active:
            raise errors.UserNotActiveError()
        
        # 4.Update username
        user.update_username(
            username=data.username, updated_at=datetime.utcnow()
        )

        # 5.Save changes
        await asyncio.gather(
            self.db_gateway.update_user(user), self.cb_gateway.update_user(user)
        )
        await asyncio.gather(
            self.db_gateway.commit(), self.cb_gateway.commit()
        )