from fastapi import FastAPI

from src.presentation.api.auth import create_auth_router
from src.presentation.api.user_movie_rating import create_user_movie_rating_router


def setup_routes(app: FastAPI) -> None:
    auth_router = create_auth_router()
    app.include_router(auth_router)

    user_movie_rating_router = create_user_movie_rating_router()
    app.include_router(user_movie_rating_router)