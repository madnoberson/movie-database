from fastapi import APIRouter

from . import routes


def create_auth_router() -> APIRouter:
    router = APIRouter(prefix="/auth", tags=["auth"])

    router.add_api_route(path="/register", endpoint=routes.register, methods=["POST"])
    router.add_api_route(path="/login", endpoint=routes.login, methods=["POST"])

    return router