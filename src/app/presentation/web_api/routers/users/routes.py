from typing import Annotated

from fastapi import Depends

from app.application.common.interfaces.identity_provider import IdentityProvider
from app.presentation.handler_factory import HandlerFactory
from app.presentation.web_api.dependencies.identity_provider import get_strict_identity_provider
from . import responses


async def get_me(
    ioc: Annotated[HandlerFactory, Depends()],
    identity_provider: Annotated[IdentityProvider, Depends(get_strict_identity_provider)]
) -> responses.GetCurrentUserOutSchema:
    async with ioc.get_current_user(identity_provider) as get_current_user:
        return await get_current_user()
