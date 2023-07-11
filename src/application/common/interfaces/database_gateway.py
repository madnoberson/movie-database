from typing import Protocol

from src.application.common.database_protocols.atomic import SupportsAtomic
from src.application.common.database_protocols import user as user_protocols
from src.application.common.database_protocols import movie as movie_protocols
from src.application.common.database_protocols import user_movie_rating as umr_protocols


class DatabaseGateway(
    SupportsAtomic,

    user_protocols.SupportsSaveUser,
    user_protocols.SupportsGetUserById,
    user_protocols.SupportsGetUserByUsername,
    user_protocols.SupportsCheckUsernameExistence,
    user_protocols.SupportsCheckUserIdExistence,

    movie_protocols.SupportsSaveMovie,
    movie_protocols.SupportsGetMovieById,
    movie_protocols.SupportsUpdateMovie,
    movie_protocols.SupportsRemoveMovie,
    movie_protocols.SupportsCheckMovieIdExistence,

    umr_protocols.SupportsSaveUserMovieRating,
    umr_protocols.SupportsUpdateUserMovieRating,
    umr_protocols.SupportsGetUserMovieRatingByUserIdAndMovieId,
    umr_protocols.SupportsCheckUserMovieRatingExistence,
    umr_protocols.SupportsRemoveUserMovieRatingByUserIdAndMovieId,

    Protocol
):
    ...