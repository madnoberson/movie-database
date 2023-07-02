from typing import Protocol

from src.application.common.filebase_protocols.movie import (
    SupportsSaveMoviePoster
)


class FilebaseGateway(
    SupportsSaveMoviePoster,
    Protocol
):
    ...