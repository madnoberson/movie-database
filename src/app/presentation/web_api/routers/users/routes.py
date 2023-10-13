from typing import Annotated

from fastapi import Depends

from app.application.queries.user import get_current_user as get_current_user_handler
from app.presentation.web_api.depends_stub import Stub
from . import responses


async def get_me(
    handler: Annotated[
        get_current_user_handler.GetCurrentUser, Depends(Stub(get_current_user_handler.GetCurrentUser))
    ]
) -> responses.GetCurrentUserOutSchema:
    return await get_current_user_handler()
