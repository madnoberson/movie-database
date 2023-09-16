from typing import Protocol

from src.application.common.protocols.database_queries import user
from src.application.common.protocols.database_queries import profile


class DatabaseQueriesGateway(
    user.SupportsCheckEmailExists,
    profile.SupportsCheckUsernameExists,
    Protocol
):
    ...