from faststream.rabbit import RabbitRouter, RabbitRoute, RabbitQueue

from . import routes


def create_user_router() -> RabbitRouter:
    handlers = [
        RabbitRoute(routes.user_created, RabbitQueue("created", True)),
        RabbitRoute(routes.username_changed, RabbitQueue("username_changed", True))
    ]

    router = RabbitRouter(prefix="user.", handlers=handlers)

    return router
