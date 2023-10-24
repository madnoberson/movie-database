from fastapi import FastAPI

from app.infrastructure.database.connection_pool import create_database_connection_pool
from app.infrastructure.database.factory import DatabaseFactoryManager
from app.infrastructure.message_broker.factory import EventBusFactory
from app.infrastructure.authentication.session.connection import create_session_gateway_connection
from app.infrastructure.authentication.session.session_gateway import SessionGateway
from app.presentation.handler_factory import HandlerFactory
from app.presentation.web_api.depends_stub import Stub
from app.main.ioc import IoC
from . import config


async def setup_dependencies(
    app: FastAPI, postgres_config: config.PostgresConfig,
    session_gateway_config: config.SessionGatewayConfig
) -> None:
    # 1.Setup `IoC`
    connection_pool = await create_database_connection_pool(postgres_config.dsn)
    ioc = IoC(
        db_factory_manager=DatabaseFactoryManager(connection_pool, connection_pool),
        event_bus_factory=EventBusFactory()
    )
    app.dependency_overrides[HandlerFactory] = lambda: ioc

    # 2.Setup `AuthSessionGateway`
    redis_connection = create_session_gateway_connection(
        host=session_gateway_config.redis_host, port=session_gateway_config.redis_port,
        db=session_gateway_config.redis_db
    )
    session_gateway = SessionGateway(redis_connection)
    app.dependency_overrides[Stub(SessionGateway)] = lambda: session_gateway