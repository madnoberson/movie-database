from typing import Protocol

from src.application.common.database_protocols.atomic import (
    SupportsAtomic
)
from src.application.common.database_protocols.movie import (
    SupportsCheckMovieIdExistence,
    SupportsRemoveMovie
)
from src.application.common.filebase_protocols.movie import (
    SupportsRemoveMoviePoster
)


class RemoveMovieCommandDBGateway(
    SupportsAtomic,
    SupportsCheckMovieIdExistence,
    SupportsRemoveMovie,
    Protocol
):
    ...


class RemoveMovieCommandFBGateway(
    SupportsRemoveMoviePoster,
    Protocol
):
    ...