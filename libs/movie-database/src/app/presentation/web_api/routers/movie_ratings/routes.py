from typing import Annotated
from uuid import UUID

from fastapi import Depends

from app.application.common.interfaces.identity_provider import IdentityProvider
from app.application.commands.movie_rating.rate_movie import InputDTO as RateMovieDTO
from app.application.commands.movie_rating.rerate_movie import InputDTO as RerateMovieDTO
from app.presentation.web_api.dependencies.identity_provider import get_strict_identity_provider
from app.presentation.handler_factory import HandlerFactory
from . import requests


async def rate_movie(
    ioc: Annotated[HandlerFactory, Depends()],
    identity_provider: Annotated[IdentityProvider, Depends(get_strict_identity_provider)],
    data: requests.RateMovieSchema,
    movie_id: UUID
) -> None:
    async with ioc.rate_movie(identity_provider) as rate_movie:
        await rate_movie(RateMovieDTO(movie_id=movie_id, rating=data.rating))


async def rerate_movie(
    ioc: Annotated[HandlerFactory, Depends()],
    identity_provider: Annotated[IdentityProvider, Depends(get_strict_identity_provider)],
    data: requests.RerateMovieSchema,
    movie_id: UUID
) -> None:
    async with ioc.rerate_movie(identity_provider) as rerate_movie:
        await rerate_movie(RerateMovieDTO(movie_id=movie_id, rating=data.rating))