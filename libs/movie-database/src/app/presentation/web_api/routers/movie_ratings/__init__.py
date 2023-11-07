from fastapi import APIRouter

from . import routes


def create_movie_ratings_router() -> APIRouter:
    router = APIRouter(prefix="/movies", tags=["movie_ratings"])

    router.add_api_route(
        path="/{movie_id}/rating", endpoint=routes.rate_movie,
        status_code=201, methods=["POST"]
    )
    router.add_api_route(
        path="/{movie_id}/rating", endpoint=routes.rerate_movie,
        status_code=204, methods=["PUT"]
    )
    router.add_api_route(
        path="/{movie_id}/rating", endpoint=routes.unrate_movie,
        status_code=204, methods=["DELETE"]
    )

    return router