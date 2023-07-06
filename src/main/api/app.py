from fastapi import FastAPI

from .config import Config
from .routes import setup_routes
from .dependencies import setup_dependencies
from .exceptions import setup_exception_handlers


def create_app(config: Config) -> FastAPI:
    app = FastAPI(
        title=config.fastapi.fastapi_title,
        description=config.fastapi.fastapi_description,
        version=config.fastapi.fastapi_version
    )

    setup_dependencies(
        app=app,
        auth_config=config.auth,
        postgres_config=config.postgres
    )
    setup_routes(app)
    setup_exception_handlers(app)

    return app
