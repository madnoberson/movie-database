from typing import Protocol

from src.application.common.protocols.cachebase import atomacity
from src.application.common.protocols.cachebase import user


class CachebaseGateway(
    atomacity.SupportsCommit,

    user.SupportsSaveUser,
    user.SupportsGetUser,
    user.SupportsUpdateUser,

    Protocol
):
    ...