from typing import Protocol

from src.application.common.protocols.database import atomacity as atomacity_db
from src.application.common.protocols.database import user as user_db
from src.application.common.protocols.database import profile as profile_db


class DatabaseGateway(
    atomacity_db.SupportsCommit,
    user_db.SupportsCheckUserExists,
    profile_db.SupportsCheckProfileExists,
    profile_db.SupportsSaveProfile,
    Protocol
):
    ...