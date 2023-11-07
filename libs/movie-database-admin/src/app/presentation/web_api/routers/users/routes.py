from typing import Annotated
from uuid import UUID

from fastapi import Depends

from app.application.common.interfaces.identity_provider import IdentityProvider
from app.application.commands.user.change_username import InputDTO as ChangeUsernameDTO
from app.presentation.web_api.dependencies.identity_provider import get_identity_provider
from app.presentation.handler_factory import HandlerFactory
from . import requests


async def change_username(
    ioc: Annotated[HandlerFactory, Depends()],
    identity_provider: Annotated[IdentityProvider, Depends(get_identity_provider)],
    data: requests.ChangeUsernameSchema,
    user_id: UUID
) -> None:
    async with ioc.change_username(identity_provider) as change_username:
        dto = ChangeUsernameDTO(user_id=user_id, username=data.username)
        await change_username(dto)