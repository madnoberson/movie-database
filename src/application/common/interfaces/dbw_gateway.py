from typing import Protocol

from src.application.common.protocols.dbw_gateway import atomacity
from src.application.common.protocols.dbw_gateway import user
from src.application.common.protocols.dbw_gateway import profile


class DatabaseWritingGateway(
    atomacity.SupportsCommit,
    
    user.SupportsCheckUserExists,
    user.SupportsSaveUser,
    user.SupportsGetUser,
    user.SupportsUpdateUser,

    profile.SupportsSaveProfile,
    profile.SupportsGetProfile,
    profile.SupportsUpdateProfile,

    Protocol
):
    ...