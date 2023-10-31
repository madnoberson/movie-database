from faststream.rabbit import RabbitBroker, RabbitRouter

from .movie_database_admin import create_movie_database_admin_router


def setup_routers(broker: RabbitBroker) -> None:
    router = RabbitRouter(prefix="movie_database.")

    router.include_router(create_movie_database_admin_router())

    broker.include_router(router)