from typing import Protocol

from src.application.common.database_interfaces.atomic import (
    SupportsAtomic
)
from src.application.common.database_interfaces.user import (
    SupportsCheckUserIdExistence
)
from src.application.common.database_interfaces.movie import (
    SupportsGetMovieById,
    SupportsUpdateMovie
)
from src.application.common.database_interfaces.user_movie_rating import (
    SupportsSaveUserMovieRating,
    SupportsCheckUserMovieRatingExistence
)


class RateMovieDBGateway(
    SupportsAtomic,
    SupportsCheckUserIdExistence,
    SupportsGetMovieById,
    SupportsUpdateMovie,
    SupportsSaveUserMovieRating,
    SupportsCheckUserMovieRatingExistence,
    Protocol
):
    ...