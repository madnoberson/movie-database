from typing import Protocol

from src.application.common.protocols.dbr_gateway import auth
from src.application.common.interfaces.password_encoder import PasswordEncoder


class DatabaseReadingGateway(
    auth.SupportsLogin,
    Protocol
):
    ...