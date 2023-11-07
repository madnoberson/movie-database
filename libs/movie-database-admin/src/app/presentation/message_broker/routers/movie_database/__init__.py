from faststream.rabbit import RabbitRouter

from .user import create_user_router


def create_movie_database_router() -> RabbitRouter:
    router = RabbitRouter(prefix="movie_database.")

    router.include_router(create_user_router())

    return router