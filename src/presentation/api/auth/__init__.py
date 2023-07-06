from fastapi import APIRouter

from .handlers import register, login
from .responses import get_register_responses, get_login_responses


def setup_routes(router: APIRouter) -> None:
    register_responses = get_register_responses()
    router.add_api_route(
        path="/register",
        endpoint=register,
        status_code=200,
        methods=["post"],
        responses=register_responses
    )

    login_responses = get_login_responses()
    router.add_api_route(
        path="/login",
        endpoint=login,
        status_code=200,
        methods=["get"],
        responses=login_responses
    )


def create_auth_router() -> APIRouter:
    auth_router = APIRouter(prefix="/auth", tags=["auth"])
    
    setup_routes(auth_router)

    return auth_router