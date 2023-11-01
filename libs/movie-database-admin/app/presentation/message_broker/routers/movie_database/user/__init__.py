from faststream.rabbit import RabbitRouter, RabbitRoute, RabbitQueue

from . import routes


def create_user_router() -> RabbitRouter:
    handlers = [
        RabbitRoute(routes.ensure_user, RabbitQueue("created", True)),
        RabbitRoute(routes.ensure_username_change, RabbitQueue("username_changed", True))
    ]

    router = RabbitRouter(prefix="user.", handlers=handlers)

    return router
