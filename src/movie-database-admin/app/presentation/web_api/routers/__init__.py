from fastapi import FastAPI, APIRouter

from .superusers import create_superusers_router


def setup_routers(app: FastAPI) -> None:
    router = APIRouter(prefix="/v1")

    router.include_router(create_superusers_router())

    app.include_router(router)