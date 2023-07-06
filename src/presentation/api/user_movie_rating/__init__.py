from fastapi import APIRouter

from .handlers import (
    rate_movie,
    reevaluate_movie, 
    remove_movie_rating
)
from .responses import (
    get_rate_movie_responses,
    get_reevaluate_movie_responses,
    get_remove_movie_rating_responses
)


__all__ = ("create_user_movie_rating_router",)


def setup_routes(router: APIRouter) -> None:
    rate_movie_responses = get_rate_movie_responses()
    router.add_api_route(
        path="/",
        endpoint=rate_movie,
        status_code=201,
        methods=["post"],
        responses=rate_movie_responses,
    )

    reevaluate_movie_responses = get_reevaluate_movie_responses()
    router.add_api_route(
        path="/{movie_id}/",
        endpoint=reevaluate_movie,
        status_code=200,
        methods=["put"],
        responses=reevaluate_movie_responses
    )

    remove_movie_rating_responses = get_remove_movie_rating_responses()
    router.add_api_route(
        path="/{movie_id}/",
        endpoint=remove_movie_rating,
        status_code=200,
        methods=["delete"],
        responses=remove_movie_rating_responses
    )


def create_user_movie_rating_router() -> APIRouter:
    user_movie_rating_router = APIRouter(
        prefix="/user/ratings", 
        tags=["user_movie_rating"]
    )

    setup_routes(user_movie_rating_router)

    return user_movie_rating_router