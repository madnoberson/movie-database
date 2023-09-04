from typing import Protocol

from src.application.common.protocols.cachebase import atomacity
from src.application.common.protocols.cachebase import user
from src.application.common.protocols.cachebase import movie
from src.application.common.protocols.cachebase import person


class CachebaseGateway(
    atomacity.SupportsCommit,

    user.SupportsSaveUser,
    user.SupportsGetUser,
    user.SupportsUpdateUser,

    movie.SupportsSaveMovie,
    movie.SupportsGetMovie,
    movie.SupportsUpdateMovie,

    person.SupportsSavePerson,
    person.SupportsGetPerson,
    person.SupportsUpdatePerson,

    Protocol
):
    ...