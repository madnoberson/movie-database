from typing import Protocol

from app.application.common.protocols.dbr_gateway import user
from app.application.common.protocols.dbr_gateway import auth


class DatabaseReadingGateway(
    user.SupportsCheckUsernameExists,
    auth.SupportsLogin,
    Protocol
):
    ...