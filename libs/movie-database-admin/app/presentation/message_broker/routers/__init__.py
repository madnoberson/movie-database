from faststream.rabbit import RabbitBroker, RabbitRouter

from .movie_database import create_movie_database_router


def setup_routers(broker: RabbitBroker) -> None:
    router = RabbitRouter(prefix="movie_database_admin.")

    router.include_router(create_movie_database_router())

    broker.include_router(router)