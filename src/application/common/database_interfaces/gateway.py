from typing import Protocol

from .atomic import SupportsAtomic
from .user import (
    SupportsSaveUser,
    SupportsGetUserById,
    SupportsGetUserByUsername,
    SupportsCheckUsernameExistence,
)
from .movie import (
    SupportsSaveMovie,
    SupportsGetMovieById
)


class DatabaseGateway(
    SupportsAtomic,
    SupportsSaveUser,
    SupportsGetUserById,
    SupportsGetUserByUsername,
    SupportsCheckUsernameExistence,
    SupportsSaveMovie,
    SupportsGetMovieById,
    Protocol
):
    ...