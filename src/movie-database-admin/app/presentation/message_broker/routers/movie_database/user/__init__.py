from faststream.rabbit import RabbitRouter, RabbitRoute

from .routes import user_created


def create_user_router() -> RabbitRouter:
    routes = [
        RabbitRoute(call=user_created, queue="created")
    ]

    router = RabbitRouter(prefix="user.", handlers=routes)

    return router
