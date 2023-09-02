from typing import Protocol

from src.application.common.protocols.filebase import atomacity
from src.application.common.protocols.filebase import user


class FilebaseGateway(
    atomacity.SupportsCommit,
    user.SupportsUpdateUserAvatar,
    Protocol
):
    ...