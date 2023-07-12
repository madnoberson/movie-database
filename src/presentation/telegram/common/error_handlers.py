from aiogram import Router
from aiogram.types.error_event import ErrorEvent
from aiogram.filters.exception import ExceptionTypeFilter

from . import errors


__all__ = ("setup_error_handlers",)


def setup_error_handlers(router: Router) -> None:
    router.errors.register(
        invalid_password_error_handler,
        ExceptionTypeFilter(errors.InvalidPasswordError)
    )
    router.errors.register(
        user_is_already_logged_in,
        ExceptionTypeFilter(errors.UserIsAlreadyLoggedIn)
    )


async def invalid_password_error_handler(event: ErrorEvent) -> None:
    await event.update.message.answer(event.exception.message)


async def user_is_already_logged_in(event: ErrorEvent) -> None:
    await event.update.message.answer(event.exception.message)