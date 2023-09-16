from typing import Protocol

from src.application.common.protocols.database_queries.user import SupportsCheckEmailExists


class DatabaseQueriesGateway(SupportsCheckEmailExists, Protocol):
    ...