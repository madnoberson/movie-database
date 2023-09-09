from typing import Protocol

from src.application.common.protocols.database import user as user_db


class DatabaseGateway(
    user_db.SupportsCheckUserExists,
    Protocol
):
    ...