from unittest.mock import Mock, AsyncMock

import pytest

from src.application.common.interfaces.database_gateway import DatabaseGateway
from src.application.common.interfaces.password_encoder import PasswordEncoder


@pytest.fixture
def db_gateway() -> DatabaseGateway:
    return AsyncMock()


@pytest.fixture
def password_encoder() -> PasswordEncoder:
    return Mock()