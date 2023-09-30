from typing import Protocol

from src.application.common.protocols.dbr_gateway import user as user_dbr


class DatabaseReadingGateway(
    user_dbr.SupportsCheckUsernameExists,
    Protocol
):
    ...