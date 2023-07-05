from typing import Protocol

from src.application.common.filebase_protocols.movie import (
    SupportsSaveMoviePoster,
    SupportsRemoveMoviePoster
)


class FilebaseGateway(
    SupportsSaveMoviePoster,
    SupportsRemoveMoviePoster,
    Protocol
):
    ...