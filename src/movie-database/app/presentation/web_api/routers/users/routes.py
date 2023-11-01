from typing import Annotated

from fastapi import Depends

from app.application.common.interfaces.identity_provider import IdentityProvider
from app.application.commands.user.change_username import InputDTO as ChangeUsernameDTO
from app.application.commands.user.change_password import InputDTO as ChangePasswordDTO
from app.presentation.handler_factory import HandlerFactory
from app.presentation.web_api.dependencies.identity_provider import get_strict_identity_provider
from . import responses
from . import requests


async def get_me(
    ioc: Annotated[HandlerFactory, Depends()],
    identity_provider: Annotated[IdentityProvider, Depends(get_strict_identity_provider)]
) -> responses.GetCurrentUserOutSchema:
    async with ioc.get_current_user(identity_provider) as get_current_user:
        return await get_current_user()


async def change_username(
    ioc: Annotated[HandlerFactory, Depends()],
    identity_provider: Annotated[IdentityProvider, Depends(get_strict_identity_provider)],
    data: requests.ChangeUsernameSchema
) -> None:
    async with ioc.change_username(identity_provider) as change_username:
        await change_username(ChangeUsernameDTO(username=data.username))


async def change_password(
    ioc: Annotated[HandlerFactory, Depends()],
    identity_provider: Annotated[IdentityProvider, Depends(get_strict_identity_provider)],
    data: requests.ChangePasswordSchema
) -> None:
    async with ioc.change_password(identity_provider) as change_password:
        dto = ChangePasswordDTO(
            old_password=data.old_password, new_password=data.new_password
        )
        await change_password(dto)