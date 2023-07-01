from typing import Protocol

from src.application.common.database_protocols.atomic import (
    SupportsAtomic
)
from src.application.common.database_protocols.movie import (
    SupportsCheckMovieIdExistence,
    SupportsRemoveMovie
)


class RemoveMovieCommandDBGateway(
    SupportsAtomic,
    SupportsCheckMovieIdExistence,
    SupportsRemoveMovie,
    Protocol
):
    ...