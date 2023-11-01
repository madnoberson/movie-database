from fastapi import FastAPI, APIRouter

from .auth import create_auth_router
from .users import create_users_router


def setup_routers(app: FastAPI) -> None:
    router = APIRouter(prefix="/v1")

    router.include_router(create_auth_router())
    router.include_router(create_users_router())

    app.include_router(router)