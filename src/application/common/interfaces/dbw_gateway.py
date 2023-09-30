from typing import Protocol

from src.application.common.protocols.dbw_gateway import atomacity
from src.application.common.protocols.dbw_gateway import user


class DatabaseWritingGateway(
    atomacity.SupportsCommit,
    
    user.SupportsCheckUserExists,
    user.SupportsSaveUser,
    user.SupportsGetUser,
    user.SupportsUpdateUser,

    Protocol
):
    ...