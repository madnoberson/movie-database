from typing import Protocol

from src.application.common.database_protocols.atomic import SupportsAtomic
from src.application.common.database_protocols.user import (
    SupportsSaveUser,
    SupportsGetUserById,
    SupportsGetUserByUsername,
    SupportsCheckUsernameExistence,
    SupportsCheckUserIdExistence
)
from src.application.common.database_protocols.movie import (
    SupportsSaveMovie,
    SupportsGetMovieById,
    SupportsUpdateMovie,
    SupportsCheckMovieIdExistence,
    SupportsRemoveMovie
)
from src.application.common.database_protocols.movie_genres import (
    SupportsSaveMovieGenres
)
from src.application.common.database_protocols.user_movie_rating import (
    SupportsSaveUserMovieRating,
    SupportsGetUserMovieRatingByUserIdAndMovieId,
    SupportsCheckUserMovieRatingExistence,
    SupportsUpdateUserMovieRating,
    SupportsRemoveUserMovieRatingByUserIdAndMovieId
)


class DatabaseGateway(
    SupportsAtomic,

    SupportsSaveUser,
    SupportsGetUserById,
    SupportsGetUserByUsername,
    SupportsCheckUsernameExistence,
    SupportsCheckUserIdExistence,

    SupportsSaveMovie,
    SupportsGetMovieById,
    SupportsUpdateMovie,
    SupportsRemoveMovie,
    SupportsCheckMovieIdExistence,

    SupportsSaveMovieGenres,

    SupportsSaveUserMovieRating,
    SupportsUpdateUserMovieRating,
    SupportsGetUserMovieRatingByUserIdAndMovieId,
    SupportsCheckUserMovieRatingExistence,
    SupportsRemoveUserMovieRatingByUserIdAndMovieId,

    Protocol
):
    ...