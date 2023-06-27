from typing import Protocol

from .atomic import SupportsAtomic
from .user import (
    SupportsSaveUser,
    SupportsGetUserById,
    SupportsGetUserByUsername,
    SupportsCheckUsernameExistence,
    SupportsCheckUserIdExistence
)
from .movie import (
    SupportsSaveMovie,
    SupportsGetMovieById,
    SupportsUpdateMovie
)
from .user_movie_rating import (
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
    SupportsSaveUserMovieRating,
    SupportsUpdateUserMovieRating,
    SupportsGetUserMovieRatingByUserIdAndMovieId,
    SupportsCheckUserMovieRatingExistence,
    SupportsRemoveUserMovieRatingByUserIdAndMovieId,
    Protocol
):
    ...