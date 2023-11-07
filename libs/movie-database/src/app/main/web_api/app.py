from fastapi import FastAPI

from app.presentation.web_api.routers import setup_routers
from app.presentation.web_api.exceptions import setup_exception_handlers
from app.main import config
from .dependencies import setup_dependencies


async def create_app(
    fastapi_config: config.FastAPIConfig, database_config: config.DatabaseConfig,
    event_bus_config: config.EventBusConfig, identity_gateway_config: config.IdentityProviderConfig
) -> FastAPI:
    app = FastAPI(
        title=fastapi_config.title, version=fastapi_config.version,
        description=fastapi_config.description, summary=fastapi_config.summary,
        docs_url=fastapi_config.docs_url, redoc_url=fastapi_config.redoc_url
    )
    await setup_dependencies(
        app=app, database_config=database_config, event_bus_config=event_bus_config,
        identity_provider_config=identity_gateway_config
    )
    setup_exception_handlers(app)
    setup_routers(app)

    return app
