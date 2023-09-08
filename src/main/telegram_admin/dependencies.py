from aiogram import Dispatcher
from asyncpg import create_pool

from src.infrastructure.presentation.db_gateway_factory.asyncpg_impl import AsyncpgDatabaseGatewayFactory
from src.infrastructure.application.password_encoder.aiobcrypt_impl import AiobcryptPasswordEncoder
from .ioc import TelegramAdminIoCImpl
from .config import PostgresConfig


async def setup_dependencies(postgres_config: PostgresConfig, dispatcher: Dispatcher) -> None:
    # 1.Setup IoC
    pool = await create_pool(dsn=postgres_config.dsn)
    db_gateway_factory = AsyncpgDatabaseGatewayFactory(pool)
    password_encoder = AiobcryptPasswordEncoder()
    dispatcher["ioc"] = TelegramAdminIoCImpl(db_gateway_factory, password_encoder)
