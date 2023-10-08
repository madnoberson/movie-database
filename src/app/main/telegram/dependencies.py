from aiogram import Dispatcher
from asyncpg import create_pool

from app.application.interactors.registration.register.interactor import Register
from app.application.queries.user.check_username_exists.handler import CheckUsernameExists
from app.application.queries.auth.login.handler import Login
from app.infrastructure.presentation.common.dbr_gateway_factory.asyncpg_impl import AsyncpgDatabaseReadingGatewayFactory
from app.infrastructure.presentation.common.dbw_gateway_factory.asyncpg_impl import AsyncpgDatabaseWritingGatewayFactory
from app.infrastructure.application.password_encoder.aiobcrypt_impl import AiobcryptPasswordEncoder
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