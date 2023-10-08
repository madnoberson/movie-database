from typing import Protocol

from app.application.common.protocols.dbw_gateway import atomacity
from app.application.common.protocols.dbw_gateway import user


class DatabaseWritingGateway(
    atomacity.SupportsCommit,
    
    user.SupportsCheckUserExists,
    user.SupportsSaveUser,
    user.SupportsGetUser,
    user.SupportsUpdateUser,

    Protocol
):
    ...