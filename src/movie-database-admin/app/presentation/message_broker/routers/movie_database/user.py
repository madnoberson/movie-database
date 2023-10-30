from typing import Annotated

from faststream import Context
from faststream.rabbit import RabbitRouter, RabbitRoute

from app.presentation.handler_factory import HandlerFactory



def create_user_router() -> RabbitRouter:
    router = RabbitRouter(prefix="user.")

    return router


async def user_created(
    ioc: Annotated[HandlerFactory, Context()]
) -> None:
    ...