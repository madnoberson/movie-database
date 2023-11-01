from fastapi import APIRouter

from . import routes


def create_superusers_router() -> APIRouter:
    router = APIRouter(prefix="/superusers", tags=["superusers"])

    router.add_api_route(
        path="", endpoint=routes.create_superuser,
        status_code=201, methods=["post"]
    )
    router.add_api_route(
        path="/password", endpoint=routes.change_superuser_password,
        status_code=204, methods=["put"]
    )

    return router