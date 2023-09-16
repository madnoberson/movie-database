from typing import Protocol

from src.application.common.protocols.database_queries.profile import SupportsCheckUsernameExists


class DatabaseQueriesGateway(SupportsCheckUsernameExists, Protocol):
    ...