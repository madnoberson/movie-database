from typing import overload, Protocol
from uuid import UUID

from src.domain.user import User
from src.application.common.protocols.database import user as user_db
from src.application.common.protocols.cachebase import atomacity as atomacity_cb
from src.application.common.protocols.cachebase import user as user_cb


__all__ = ["SupportsGetAndCacheUser"]


class DatabaseGateway(
    user_db.SupportsGetUser,
    Protocol
):
    ...


class CachebaseGateway(
    atomacity_cb.SupportsCommit,
    user_cb.SupportsGetUser,
    user_cb.SupportsSaveUser,
    Protocol
):
    ...


class SupportsGetAndCacheUser:

    @overload
    async def get_and_cache_user(
        self, db_gateway: DatabaseGateway, cb_gateway: CachebaseGateway, user_id: UUID
    ) -> User | None:
        ...

    @overload
    async def get_and_cache_user(
        self, db_gateway: DatabaseGateway, cb_gateway: CachebaseGateway, email: str
    ) -> User | None:
        ...
    
    async def get_and_cache_user(
        self, db_gateway: DatabaseGateway, cb_gateway: CachebaseGateway,
        user_id: UUID | None = None, email: str | None = None
    ) -> User | None:
        # 1.Get user from cachebase
        user = await cb_gateway.get_user(user_id=user_id, email=email)
        if user is not None: return user

        # 2.Get user from database if user not in cachebase
        user = await db_gateway.get_user(user_id=user_id, email=email)
        if user is not None:
            await cb_gateway.save_user(user)
            await cb_gateway.commit()

        return user