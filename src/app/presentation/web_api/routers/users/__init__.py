from fastapi import APIRouter

from . import routes

def create_users_router() -> APIRouter:
    router = APIRouter(prefix="/users", tags=["users"])

    router.add_api_route(path="/me", endpoint=routes.get_me)

    return router