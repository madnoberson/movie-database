from typing import Protocol

from src.application.common.protocols.presenatation_database import user
from src.application.common.protocols.presenatation_database import profile


class PresentationDatabaseGateway(
    user.SupportsCheckEmailExists,
    profile.SupportsCheckUsernameExists,
    Protocol
):
    ...