from typing import Protocol

from src.application.common.protocols.dbr_gateway import user


class DatabaseReadingGateway(
    user.SupportsCheckUsernameExists,
    Protocol
):
    ...