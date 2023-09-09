from typing import Protocol

from src.application.common.protocols.database import profile as profile_db


class DatabaseGateway(
    profile_db.SupportsCheckProfileExists,
    Protocol
):
    ...