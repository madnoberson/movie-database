from typing import Annotated

from faststream import Context

from app.application.commands.movie.ensure_movie import InputDTO as EnsureMovieDTO
from app.presentation.handler_factory import HandlerFactory
from . import events


async def ensure_movie(
    ioc: Annotated[HandlerFactory, Context()],
    event: events.MovieCreated
) -> None:
    async with ioc.ensure_movie() as ensure_movie:
        dto = EnsureMovieDTO(
            movie_id=event.movie_id, en_name=event.en_name,
            created_at=event.created_at
        )
        await ensure_movie(dto)