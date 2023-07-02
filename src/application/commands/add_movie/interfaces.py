from typing import Protocol

from src.application.common.database_protocols.atomic import (
    SupportsAtomic
)
from src.application.common.database_protocols.movie import (
    SupportsSaveMovie
)
from src.application.common.database_protocols.movie_genres import (
    SupportsSaveMovieGenres
)
from src.application.common.filebase_protocols.movie import (
    SupportsSaveMoviePoster
)


class AddMovieCommandDBGateway(
    SupportsAtomic,
    SupportsSaveMovie,
    SupportsSaveMovieGenres,
    Protocol
):
    ...


class AddMovieCommandFBGateway(
    SupportsSaveMoviePoster,
    Protocol
):
    ...