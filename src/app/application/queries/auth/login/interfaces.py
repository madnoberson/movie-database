from typing import Protocol

from app.application.common.protocols.dbr_gateway import auth
from app.application.common.interfaces.password_encoder import PasswordEncoder


class DatabaseReadingGateway(
    auth.SupportsLogin,
    Protocol
):
    ...