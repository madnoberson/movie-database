from typing import Protocol

from .atomic import SupportsAtomic
from .user import (
    SupportsSaveUser,
    SupportsGetUserById,
    SupportsGetUserByUsername
)


class DatabaseGateway(
    SupportsAtomic,
    SupportsSaveUser,
    SupportsGetUserById,
    SupportsGetUserByUsername,
    Protocol
):
    ...