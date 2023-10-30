from typing import Annotated

from faststream import Context

from app.application.commands.user.ensure_user import InputDTO as EnsureUserDTO
from app.presentation.handler_factory import HandlerFactory
from . import events


async def user_created(
    ioc: Annotated[HandlerFactory, Context()],
    event: events.UserCreated
) -> None:
    async with ioc.ensure_user() as ensure_user:
        dto = EnsureUserDTO(
            user_id=event.user_id, username=event.username,
            created_at=event.created_at
        )
        await ensure_user(dto)