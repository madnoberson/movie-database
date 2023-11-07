from fastapi import APIRouter

from . import routes


def create_movies_router() -> APIRouter:
    router = APIRouter(prefix="/movies", tags=["movies"])

    router.add_api_route(
        path="", endpoint=routes.create_movie,
        status_code=201, methods=["post"]
    )

    return router