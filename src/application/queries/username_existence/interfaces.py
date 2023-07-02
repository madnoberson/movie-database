from typing import Protocol

from src.application.common.database_protocols.user import (
    SupportsCheckUsernameExistence
)


class UsernameExistenceDBGateway(
    SupportsCheckUsernameExistence,
    Protocol
):
    ...