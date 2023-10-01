from aiogram import Dispatcher
from asyncpg import create_pool

from src.application.interactors.registration.register.interactor import Register
from src.application.queries.user.check_username_exists.handler import CheckUsernameExists
from src.application.queries.auth.login.handler import Login
from src.infrastructure.presentation.common.dbr_gateway_factory.asyncpg_impl import AsyncpgDatabaseReadingGatewayFactory
from src.infrastructure.presentation.common.dbw_gateway_factory.asyncpg_impl import AsyncpgDatabaseWritingGatewayFactory
from src.infrastructure.application.password_encoder.aiobcrypt_impl import AiobcryptPasswordEncoder
from .handler_factories import setup_handler_factories
from .config import PostgresConfig


async def setup_dependencies(postgres_config: PostgresConfig, dispatcher: Dispatcher) -> None:
    pool = await create_pool(dsn=postgres_config.dsn)
    
    handlers = [Register, CheckUsernameExists, Login]
    dependencies = [
        AsyncpgDatabaseWritingGatewayFactory(pool), AsyncpgDatabaseReadingGatewayFactory(pool),
        AiobcryptPasswordEncoder()
    ]

    setup_handler_factories(dispatcher, handlers, dependencies)