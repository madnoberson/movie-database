from typing import Annotated

from fastapi import Depends

from app.application.common.interfaces.identity_provider import IdentityProvider
from app.application.commands.enrichment_task.create_task import InputDTO as CreateEnrichmentTaskDTO
from app.presentation.handler_factory import HandlerFactory
from app.presentation.web_api.dependencies.identity_provider import get_strict_identity_provider
from . import requests
from . import responses


async def create_enrichment_task(
    ioc: Annotated[HandlerFactory, Depends()],
    identity_provider: Annotated[IdentityProvider, Depends(get_strict_identity_provider)],
    data: requests.CreateEnrichmentTaskSchema
) -> responses.CreateEnrichmentTaskOutSchema:
    async with ioc.create_enrichment_task(identity_provider) as create_enrichment_task:
        dto = CreateEnrichmentTaskDTO(kinopoisk_id=data.kinopisk_id)
        return await create_enrichment_task(dto)


