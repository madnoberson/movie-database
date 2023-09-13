from typing import Protocol

from src.application.common.protocols.presenatation_database.profile import SupportsCheckUsernameExists


class PresenstationDatabaseGateway(SupportsCheckUsernameExists, Protocol):
    ...