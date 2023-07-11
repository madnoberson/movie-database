from aiogram import Router
from aiogram.types import ErrorEvent
from aiogram.filters.exception import ExceptionTypeFilter

from . import errors


__all__ = ("setup_error_handlers",)


def setup_error_handlers(router: Router) -> None:
    router.errors.register(
        invalid_title_error_handler,
        ExceptionTypeFilter(errors.InvalidTitleError)
    )
    router.errors.register(
        invalid_release_date_error_handler,
        ExceptionTypeFilter(errors.InvalidReleaseDateError)
    )
    router.errors.register(
        invalid_poster_error_handler,
        ExceptionTypeFilter(errors.InvalidPosterError)
    )


async def invalid_title_error_handler(event: ErrorEvent) -> None:
    await event.update.message.answer(event.exception.message)


async def invalid_release_date_error_handler(event: ErrorEvent) -> None:
    await event.update.message.answer(event.exception.message)


async def invalid_poster_error_handler(event: ErrorEvent) -> None:
    await event.update.message.answer(event.exception.message)