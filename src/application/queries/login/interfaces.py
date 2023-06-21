from typing import Protocol

from src.application.common.database_intefaces.user import (
    SupportsGetUserByUsername
)


class LoginQueryDBGateway(
    SupportsGetUserByUsername,
    Protocol
):
    ...