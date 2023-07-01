from typing import Protocol

from src.application.common.database_protocols.user import (
    SupportsGetUserByUsername
)


class LoginQueryDBGateway(
    SupportsGetUserByUsername,
    Protocol
):
    ...