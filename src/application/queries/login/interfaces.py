from typing import Protocol

from src.application.common.database_interfaces.user import (
    SupportsGetUserByUsername
)


class LoginQueryDBGateway(
    SupportsGetUserByUsername,
    Protocol
):
    ...