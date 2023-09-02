import asyncio
from logging import getLogger
from dataclasses import dataclass
from datetime import datetime

from src.application.common import utils
from src.application.common import mixins
from . import dto
from . import errors
from . import interfaces


logger = getLogger("UpdateAvatar")


@dataclass(frozen=True, slots=True)
class UpdateAvatar(mixins.SupportsGetAndCacheUser):
    
    db_gateway: interfaces.CachebaseGateway
    cb_gateway: interfaces.CachebaseGateway
    fb_gateway: interfaces.FilebaseGateway

    @utils.handle_unexpected_exceptions(
        logger, errors.UserDoesNotExistError, errors.UserNotActiveError,
        errors.UserNotConfirmedError
    )
    async def __call__(self, data: dto.UpdateAvatarDTO) -> None:
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
        
        # 4.Update user avatar
        user.update_avatar(
            avatar_url=f"{user.id.hex}-avatar", updated_at=datetime.utcnow()
        )

        # 5.Save changes
        await asyncio.gather(
            self.db_gateway.update_user(user), self.cb_gateway.update_user(user),
            self.fb_gateway.update_user_avatar(key=user.avatar_url, avatar=data.avatar)
        )
        await asyncio.gather(
            self.db_gateway.commit(), self.cb_gateway.commit(), self.fb_gateway.commit()
        )