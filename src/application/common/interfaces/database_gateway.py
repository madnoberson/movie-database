from typing import Protocol

from src.application.common.protocols.database import atomacity
from src.application.common.protocols.database import user
from src.application.common.protocols.database import profile


class DatabaseGateway(
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