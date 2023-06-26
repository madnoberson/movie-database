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
    SupportsGetUserMovieRatingByUserIdAndMovieId,
    SupportsUpdateUserMovieRating
)


class ReevaluateMovieCommandDBGateway(
    SupportsAtomic,
    SupportsCheckUserIdExistence,
    SupportsGetMovieById,
    SupportsUpdateMovie,
    SupportsGetUserMovieRatingByUserIdAndMovieId,
    SupportsUpdateUserMovieRating,
    Protocol
):
    ...