from typing import Protocol

from src.application.common.database_protocols.atomic import (
    SupportsAtomic
)
from src.application.common.database_protocols.movie import (
    SupportsSaveMovie
)


class AddMovieCommandDBGateway(
    SupportsSaveMovie,
    SupportsAtomic,
    Protocol
):
    ...