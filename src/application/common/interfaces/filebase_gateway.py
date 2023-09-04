from typing import Protocol

from src.application.common.protocols.filebase import atomacity
from src.application.common.protocols.filebase import user
from src.application.common.protocols.filebase import movie
from src.application.common.protocols.filebase import person


class FilebaseGateway(
    atomacity.SupportsCommit,

    user.SupportsSaveUserAvatar,
    user.SupportsUpdateUserAvatar,

    movie.SupportsSaveMoviePoster,
    movie.SupportsUpdateMoviePoster,

    person.SupportsSavePersonAvatar,
    person.SupportsUpdatePersonAvatar,
    
    Protocol
):
    ...