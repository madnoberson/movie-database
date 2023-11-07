from typing import Annotated

from fastapi import Depends

from app.application.common.interfaces.identity_provider import IdentityProvider
from app.application.commands.movie.create_movie import InputDTO as CreateMovieDTO
from app.presentation.web_api.dependencies.identity_provider import get_identity_provider
from app.presentation.handler_factory import HandlerFactory
from . import requests
from . import responses


async def create_movie(
    ioc: Annotated[HandlerFactory, Depends()],
    identity_provider: Annotated[IdentityProvider, Depends(get_identity_provider)],
    data: requests.CreateMovieSchema
) -> None:
    async with ioc.create_movie(identity_provider) as create_movie:
        result = await create_movie(CreateMovieDTO(en_name=data.en_name))
    return responses.CreateMovieOutSchema(movie_id=result.movie_id)
