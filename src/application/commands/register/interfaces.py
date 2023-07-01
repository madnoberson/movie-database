from typing import Protocol

from src.application.common.database_protocols.user import (
    SupportsSaveUser,
    SupportsGetUserByUsername
)
from src.application.common.database_protocols.atomic import (
    SupportsAtomic
)


class RegisterCommandDBGateway(
    SupportsAtomic,
    SupportsSaveUser,
    SupportsGetUserByUsername,
    Protocol
):
    ...
