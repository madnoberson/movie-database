from faststream.rabbit import RabbitRouter, RabbitRoute, RabbitQueue

from . import routes


def create_user_router() -> RabbitRouter:
    handlers = [
        RabbitRoute(call=routes.user_created, queue=RabbitQueue("created", True))
    ]

    router = RabbitRouter(prefix="user.", handlers=handlers)

    return router
