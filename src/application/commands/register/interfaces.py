from typing import Protocol

from src.application.common.database_intefaces.user import (
    SupportsSaveUser,
    SupportsGetUserByUsername
)
from src.application.common.database_intefaces.atomic import (
    SupportsAtomic
)


class RegisterCommandDBGateway(
    SupportsAtomic,
    SupportsSaveUser,
    SupportsGetUserByUsername,
    Protocol
):
    ...
