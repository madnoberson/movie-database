from typing import Protocol

from src.application.common.database_interfaces.user import (
    SupportsCheckUsernameExistence
)


class UsernameExistenceDBGateway(
    SupportsCheckUsernameExistence,
    Protocol
):
    ...