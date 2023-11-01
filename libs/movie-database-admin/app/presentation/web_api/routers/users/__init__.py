from fastapi import APIRouter

from . import routes


def create_users_router() -> APIRouter:
    router = APIRouter(prefix="/users", tags=["users"])

    router.add_api_route(
        path="/{user_id}", endpoint=routes.change_username,
        status_code=204, methods=["put"]
    )

    return router