from fastapi import FastAPI

from app.presentation.web_api.routers import setup_routers
from app.presentation.web_api.exceptions import setup_exception_handlers
from .dependencies import setup_dependencies
from . import config


async def create_app(
    fastapi_config: config.FastAPIConfig, postgres_config: config.PostgresConfig,
    session_gateway_config: config.SessionGatewayConfig
) -> FastAPI:
    app = FastAPI(
        title=fastapi_config.title, version=fastapi_config.version,
        description=fastapi_config.description, summary=fastapi_config.summary,
        docs_url=fastapi_config.docs_url, redoc_url=fastapi_config.redoc_url
    )
    await setup_dependencies(
        app=app, postgres_config=postgres_config,
        session_gateway_config=session_gateway_config
    )
    setup_exception_handlers(app)
    setup_routers(app)

    return app
