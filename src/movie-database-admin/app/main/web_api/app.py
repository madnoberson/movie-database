from fastapi import FastAPI

from app.presentation.web_api.routers import setup_routers
from app.main import config
from .dependencies import setup_dependencies


async def create_app(
    fastapi_config: config.FastAPIConfig,
    database_config: config.DatabaseConfig,
    identity_provider_config: config.IdentityProviderConfig
) -> FastAPI:
    app = FastAPI(
        title=fastapi_config.title, version=fastapi_config.version,
        description=fastapi_config.description, summary=fastapi_config.summary,
        docs_url=fastapi_config.docs_url, redoc_url=fastapi_config.redoc_url
    )
    setup_routers(app)
    await setup_dependencies(
        app=app, database_config=database_config,
        identity_provider_config=identity_provider_config
    )
    
    return app