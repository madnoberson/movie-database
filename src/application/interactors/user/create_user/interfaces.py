from typing import Protocol

from src.application.common.interfaces.password_encoder import PasswordEncoder
from src.application.common.protocols.database.atomacity import SupportsCommit
from src.application.common.protocols.database import user as user_db_protocols


class DatabaseGateway(
    SupportsCommit,
    user_db_protocols.SupportsEnsureUserExists,
    user_db_protocols.SupportsSaveUser,
    Protocol
):
    ...