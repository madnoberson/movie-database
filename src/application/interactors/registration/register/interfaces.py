from typing import Protocol

from src.application.common.protocols.dbw_gateway import atomacity as atomacity_dbw
from src.application.common.protocols.dbw_gateway import user as user_dbw
from src.application.common.protocols.dbw_gateway import profile as profile_dbw
from src.application.common.interfaces.password_encoder import PasswordEncoder


class DatabaseWritingGateway(
    atomacity_dbw.SupportsCommit,
    user_dbw.SupportsCheckUserExists,
    user_dbw.SupportsSaveUser,
    profile_dbw.SupportsSaveProfile,
    Protocol
):
    ...