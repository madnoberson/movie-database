from fastapi import APIRouter

from . import routes


def create_auth_router() -> APIRouter:
    router = APIRouter(prefix="/auth", tags=["auth"])

    router.add_api_route(
        path="/login", endpoint=routes.login,
        methods=["post"]
    )

    return router