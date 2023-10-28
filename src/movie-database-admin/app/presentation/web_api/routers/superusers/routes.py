from typing import Annotated

from fastapi import Depends

from app.application.common.interfaces.identity_provider import IdentityProvider
from app.application.commands.superuser.create_superuser import InputDTO as CreateUserDTO
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
        dto = CreateUserDTO(
            username=data.username, email=data.email,
            password=data.password, permissions=data.permissions
        )
        result = await create_superuser(dto)
    return responses.CreateSuperuserOutSchema(superuser_id=result.superuser_id)
    