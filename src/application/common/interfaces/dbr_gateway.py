from typing import Protocol

from src.application.common.protocols.dbr_gateway import user
from src.application.common.protocols.dbr_gateway import auth


class DatabaseReadingGateway(
    user.SupportsCheckUsernameExists,
    auth.SupportsLogin,
    Protocol
):
    ...