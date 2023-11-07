from faststream.rabbit import RabbitRouter

from .user import create_user_router
from .movie import create_movie_router


def create_movie_database_admin_router() -> RabbitRouter:
    router = RabbitRouter(prefix="movie_database_admin.")

    router.include_router(create_user_router())
    router.include_router(create_movie_router())

    return router