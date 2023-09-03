from typing import Protocol

from src.application.common.protocols.database import atomacity
from src.application.common.protocols.database import user
from src.application.common.protocols.database import movie


class DatabaseGateway(
    atomacity.SupportsCommit,

    user.SupportsSaveUser,
    user.SupportsGetUser,
    user.SupportsUpdateUser,
    
    movie.SupportsSaveMovie,
    movie.SupportsGetMovie,
    movie.SupportsUpdateMovie,

    Protocol
):
    ...