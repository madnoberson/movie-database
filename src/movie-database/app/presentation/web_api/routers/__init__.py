from fastapi import FastAPI

from .auth import create_auth_router
from .users import create_users_router
from .enrichment import create_enrichment_router


def setup_routers(app: FastAPI) -> None:
    app.include_router(create_auth_router())
    app.include_router(create_users_router())
    app.include_router(create_enrichment_router())