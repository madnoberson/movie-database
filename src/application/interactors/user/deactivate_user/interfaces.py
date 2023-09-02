from typing import Protocol

from src.application.common.protocols.database import atomacity as atomacity_db
from src.application.common.protocols.database import user as user_db
from src.application.common.protocols.cachebase import atomacity as atomacity_cb
from src.application.common.protocols.cachebase import user as user_cb


class DatabaseGateway(
    atomacity_db.SupportsCommit,
    user_db.SupportsGetUser,
    user_db.SupportsUpdateUser,
    Protocol
):
    ...


class CachebaseGateway(
    atomacity_cb.SupportsCommit,
    user_cb.SupportsGetUser,
    user_cb.SupportsSaveUser,
    user_cb.SupportsUpdateUser,
    Protocol
):
    ...
