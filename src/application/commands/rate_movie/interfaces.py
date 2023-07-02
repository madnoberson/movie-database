from typing import Protocol

from src.application.common.database_protocols.atomic import (
    SupportsAtomic
)
from src.application.common.database_protocols.user import (
    SupportsCheckUserIdExistence
)
from src.application.common.database_protocols.movie import (
    SupportsGetMovieById,
    SupportsUpdateMovie
)
from src.application.common.database_protocols.user_movie_rating import (
    SupportsSaveUserMovieRating,
    SupportsCheckUserMovieRatingExistence
)


class RateMovieCommandDBGateway(
    SupportsAtomic,
    SupportsCheckUserIdExistence,
    SupportsGetMovieById,
    SupportsUpdateMovie,
    SupportsSaveUserMovieRating,
    SupportsCheckUserMovieRatingExistence,
    Protocol
):
    ...