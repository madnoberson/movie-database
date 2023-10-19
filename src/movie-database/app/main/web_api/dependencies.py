from fastapi import FastAPI

from app.infrastructure.database.connection_pool import create_connection_pool
from app.infrastructure.database.factories import AsyncpgFactoryManager
from app.infrastructure.authentication.session import create_redis_connection, AuthSessionGateway
from app.presentation.handler_factory import HandlerFactory
from app.presentation.web_api.depends_stub import Stub
from app.main.ioc import IoC
from . import config


async def setup_dependencies(
    app: FastAPI, postgres_config: config.PostgresConfig,
    redis_config: config.RedisConfig
) -> None:
    # 1.Setup IoC
    connection_pool = await create_connection_pool(postgres_config.dsn)
    factories_manager = AsyncpgFactoryManager(connection_pool, connection_pool)
    app.dependency_overrides[HandlerFactory] = lambda: IoC(factories_manager)

    # 2.Setup auth session gateway
    redis_connection = create_redis_connection(redis_config.host, redis_config.port, redis_config.db)
    auth_session_gateway = AuthSessionGateway(redis_connection)
    app.dependency_overrides[Stub(AuthSessionGateway)] = lambda: auth_session_gateway