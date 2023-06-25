from typing import Protocol

from src.application.common.database_interfaces.atomic import (
    SupportsAtomic
)
from src.application.common.database_interfaces.movie import (
    SupportsSaveMovie
)


class AddMovieCommandDBGateway(
    SupportsSaveMovie,
    SupportsAtomic,
    Protocol
):
    ...