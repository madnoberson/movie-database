from fastapi import APIRouter

from . import routes

def create_users_router() -> APIRouter:
    router = APIRouter(prefix="/users", tags=["users"])

    router.add_api_route(
        path="/me", endpoint=routes.get_me, methods=["get"]
    )
    router.add_api_route(
        path="/me/username", endpoint=routes.change_username,
        status_code=204, methods=["put"]
    )
    router.add_api_route(
        path="/me/password", endpoint=routes.change_password,
        status_code=204, methods=["put"]
    )

    return router