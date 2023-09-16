from typing import Protocol

from src.application.common.protocols.database import atomacity as atomacity_db
from src.application.common.protocols.database import user as user_db
from src.application.common.interfaces.password_encoder import PasswordEncoder


class DatabaseGateway(
    atomacity_db.SupportsCommit,
    user_db.SupportsCheckUserExists,
    user_db.SupportsSaveUser,
    Protocol
):
    ...