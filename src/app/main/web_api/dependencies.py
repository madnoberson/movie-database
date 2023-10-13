from fastapi import FastAPI

from app.infrastructure.database.connection_pool import create_connection_pool
from . import config


async def setup_dependencies(
    app: FastAPI, postgres_config: config.PostgresConfig,
    redis_config: config.RedisConfig
) -> None:
    ...