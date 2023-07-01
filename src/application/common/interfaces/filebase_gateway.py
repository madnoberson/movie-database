from typing import Protocol

from src.application.common.filebase_protocols.image import (
    SupportsSaveImage
)


class FilebaseGateway(
    SupportsSaveImage,
    Protocol
):
    ...