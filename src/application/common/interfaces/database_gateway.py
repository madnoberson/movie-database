from typing import Protocol

from src.application.common.protocols.database import atomacity as atomacity_protocols
from src.application.common.protocols.database import user as user_protocols


class DatabaseGateway(
    atomacity_protocols.SupportsCommit,

    user_protocols.SupportsEnsureUserExists,
    user_protocols.SupportsSaveUser,
    user_protocols.SupportsGetUser,
    user_protocols.SupportsUpdateUser,
    user_protocols.SupportsDeleteUser,

    Protocol
):
    ...