from typing import Annotated

from fastapi import Depends

from app.application.common.interfaces.identity_provider import IdentityProvider
from app.application.commands.adding_task.create_task import InputDTO as CreateAddingTaskDTO
from app.presentation.handler_factory import HandlerFactory
from app.presentation.web_api.dependencies.identity_provider import get_strict_identity_provider
from . import requests
from . import responses


async def create_adding_task(
    ioc: Annotated[HandlerFactory, Depends()],
    identity_provider: Annotated[IdentityProvider, Depends(get_strict_identity_provider)],
    data: requests.CreateAddingTaskSchema
) -> responses.CreateAddingTaskOutSchema:
    async with ioc.create_adding_task(identity_provider) as create_adding_task:
        dto = CreateAddingTaskDTO(kinopoisk_id=data.kinopisk_id, adding_type=data.adding_type)
        return await create_adding_task(dto)


