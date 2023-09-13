from typing import Protocol

from src.application.common.protocols.presenatation_database.user import SupportsCheckEmailExists


class PresentationDatabaseGateway(SupportsCheckEmailExists, Protocol):
    ...