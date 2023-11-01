from typing import Annotated

from fastapi import Depends

from app.application.common.interfaces.identity_provider import IdentityProvider
from app.application.commands.superuser.create_superuser import InputDTO as CreateSuperuserDTO
from app.application.commands.superuser.change_password import InputDTO as ChangeSuperuserPasswordDTO
from app.presentation.handler_factory import HandlerFactory
from app.presentation.web_api.dependencies.identity_provider import get_identity_provider
from . import requests
from . import responses


async def create_superuser(
    ioc: Annotated[HandlerFactory, Depends()],
    identity_provider: Annotated[IdentityProvider, Depends(get_identity_provider)],
    data: requests.CreateSuperuserSchema
) -> responses.CreateSuperuserOutSchema:
    async with ioc.create_superuser(identity_provider) as create_superuser:
        dto = CreateSuperuserDTO(
            username=data.username, email=data.email,
            password=data.password, permissions=data.permissions
        )
        result = await create_superuser(dto)
    return responses.CreateSuperuserOutSchema(superuser_id=result.superuser_id)


async def change_superuser_password(
    ioc: Annotated[HandlerFactory, Depends()],
    identity_provider: Annotated[IdentityProvider, Depends(get_identity_provider)],
    data: requests.ChangeSuperuserPasswordSchema
) -> None:
    async with ioc.change_superuser_password(identity_provider) as change_superuser_password:
        dto = ChangeSuperuserPasswordDTO(
            superuser_id=data.superuser_id, new_password=data.new_password
        )
        await change_superuser_password(dto)