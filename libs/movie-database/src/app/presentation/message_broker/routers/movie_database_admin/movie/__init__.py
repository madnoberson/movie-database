from faststream.rabbit import RabbitRouter, RabbitRoute, RabbitQueue

from . import routes


def create_movie_router() -> RabbitRouter:
    handlers = [
        RabbitRoute(routes.ensure_movie, RabbitQueue("created", True))
    ]

    router = RabbitRouter(prefix="movie.", handlers=handlers)

    return router
