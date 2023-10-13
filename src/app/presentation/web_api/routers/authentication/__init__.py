from fastapi import APIRouter

from . import routes


def create_authentication_router() -> APIRouter:
    router = APIRouter(prefix="/auth", tags=["auth"])

    router.add_api_route(path="/register", endpoint=routes.register)
    router.add_api_route(path="/login", endpoint=routes.login)

    return router