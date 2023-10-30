from faststream import FastStream

from app.domain.services.access import AccessService
from app.infrastructure.database.connection_pool import create_database_connection_pool
from app.infrastructure.database.factory import DatabaseFactoryManager
from app.main.ioc import IoC
from app.main import config


async def setup_dependencies(
    app: FastStream, database_config: config.DatabaseConfig
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

    ioc = IoC(db_factory_manager=db_factory_manager, access_service=AccessService())
    app.context.set_global("ioc", ioc)