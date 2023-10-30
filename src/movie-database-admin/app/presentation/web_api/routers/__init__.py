from fastapi import FastAPI, APIRouter

from .superusers import create_superusers_router
from .auth import create_auth_router


def setup_routers(app: FastAPI) -> None:
    router = APIRouter(prefix="/v1")

    router.include_router(create_superusers_router())
    router.include_router(create_auth_router())

    app.include_router(router)