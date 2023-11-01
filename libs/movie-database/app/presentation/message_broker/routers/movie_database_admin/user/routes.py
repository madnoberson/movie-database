from typing import Annotated

from faststream import Context

from app.application.commands.user.ensure_username_change import InputDTO as EnsureUsernameChangeDTO
from app.presentation.handler_factory import HandlerFactory
from . import events

    
async def ensure_username_change(
    ioc: Annotated[HandlerFactory, Context()],
    event: events.UsernameChanged
) -> None:
    async with ioc.ensure_username_change() as ensure_username_change:
        dto = EnsureUsernameChangeDTO(
            user_id=event.user_id, new_username=event.new_username
        )
        await ensure_username_change(dto)