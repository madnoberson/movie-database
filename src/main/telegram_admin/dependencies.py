from aiogram import Dispatcher
from asyncpg import create_pool

from src.infrastructure.presentation.common.db_gateway_factory.asyncpg_impl import AsyncpgDatabaseGatewayFactory
from src.infrastructure.application.password_encoder.aiobcrypt_impl import AiobcryptPasswordEncoder
from .interactor_factories import setup_interactor_factories
from .config import PostgresConfig


async def setup_dependencies(postgres_config: PostgresConfig, dispatcher: Dispatcher) -> None:
    # 1.Setup interactor factories
    pool = await create_pool(dsn=postgres_config.dsn)
    setup_interactor_factories(
        dispatcher=dispatcher, interactors=[],
        db_gateway_factory=AsyncpgDatabaseGatewayFactory(pool),
        password_encoder=AiobcryptPasswordEncoder()
    )

