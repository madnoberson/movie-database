from typing import Protocol

from app.application.common.protocols.dbw_gateway import atomacity as atomacity_dbw
from app.application.common.protocols.dbw_gateway import user as user_dbw
from app.application.common.interfaces.password_encoder import PasswordEncoder


class DatabaseWritingGateway(
    atomacity_dbw.SupportsCommit,
    user_dbw.SupportsCheckUserExists,
    user_dbw.SupportsSaveUser,
    Protocol
):
    ...