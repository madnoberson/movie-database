from typing import Protocol

from src.application.common.database_interfaces.user import (
    SupportsSaveUser,
    SupportsGetUserByUsername
)
from src.application.common.database_interfaces.atomic import (
    SupportsAtomic
)


class RegisterCommandDBGateway(
    SupportsAtomic,
    SupportsSaveUser,
    SupportsGetUserByUsername,
    Protocol
):
    ...
