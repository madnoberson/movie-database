from fastapi import FastAPI

from app.domain.services.movie_rating import MovieRatingService
from app.domain.services.achievement import AchievementService
from app.infrastructure.database.connection_pool import create_database_connection_pool
from app.infrastructure.database.factory import DatabaseFactoryManager
from app.infrastructure.message_broker.connection import create_event_bus_connection
from app.infrastructure.message_broker.factory import EventBusFactory
from app.infrastructure.authentication.session.connection import create_session_gateway_connection
from app.infrastructure.authentication.session.session_gateway import SessionGateway
from app.presentation.handler_factory import HandlerFactory
from app.presentation.web_api.dependencies.depends_stub import Stub
from app.main.ioc import IoC
from app.main import config


async def setup_dependencies(
    app: FastAPI, database_config: config.DatabaseConfig, event_bus_config: config.EventBusConfig,
    identity_provider_config: config.IdentityProviderConfig
) -> None:
    # 1.Setup `IoC`
    db_connection_pool = await create_database_connection_pool(
        postgres_dsn=database_config.postgres_dsn, min_size=database_config.min_connections,
        max_size=database_config.max_connections, max_queries=database_config.max_queries,
        max_inactive_connection_lifetime=database_config.max_inactive_connection_lifetime
    )
    db_factory_manager = DatabaseFactoryManager(
        repo_connection_pool=db_connection_pool, reader_connection_pool=db_connection_pool
    )

    event_bus_connection = await create_event_bus_connection(
        rq_host=event_bus_config.rq_host, rq_port=event_bus_config.rq_port,
        rq_login=event_bus_config.rq_login, rq_password=event_bus_config.rq_password
    )
    event_bus_factory = EventBusFactory(event_bus_connection)

    app.dependency_overrides[HandlerFactory] = lambda: IoC(
        db_factory_manager=db_factory_manager, event_bus_factory=event_bus_factory,
        movie_rating_service=MovieRatingService(), achievement_service=AchievementService()
    )

    # 2.Setup `SessionGateway`
    session_gateway_connection = create_session_gateway_connection(
        redis_host=identity_provider_config.session_gateway_redis_host,
        redis_port=identity_provider_config.session_gateway_redis_port,
        redis_db=identity_provider_config.session_gateway_redis_db,
        redis_password=identity_provider_config.session_gateway_redis_password
    )
    app.dependency_overrides[Stub(SessionGateway)] = lambda: SessionGateway(
        connection=session_gateway_connection,
        session_lifetime=identity_provider_config.session_gateway_session_lifetime
    )