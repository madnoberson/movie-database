from fastapi import FastAPI

from app.presentation.web_api.routers.authentication import create_authentication_router
from app.presentation.web_api.routers.users import create_users_router
from .dependencies import setup_dependencies
from . import config


def setup_routers(app: FastAPI) -> None:
    app.include_router(create_authentication_router())
    app.include_router(create_users_router())


async def create_app(
    fastapi_config: config.FastapiConfig, postgres_config: config.PostgresConfig,
    redis_config: config.RedisConfig
) -> FastAPI:
    app = FastAPI(
        title=fastapi_config.title, version=fastapi_config.version,
        description=fastapi_config.description, summary=fastapi_config.summary,
        docs_url=fastapi_config.docs_url, redoc_url=fastapi_config.redoc_url
    )
    await setup_dependencies(postgres_config=postgres_config, redis_config=redis_config)
    setup_routers(app)

    return app
