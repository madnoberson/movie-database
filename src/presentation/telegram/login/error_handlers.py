from aiogram import Router
from aiogram.types.error_event import ErrorEvent
from aiogram.filters.exception import ExceptionTypeFilter

from src.application.queries.login import errors


__all__ = ("setup_error_handlers",)


def setup_error_handlers(router: Router) -> None:
    router.errors.register(
        username_does_not_exist_error_handler,
        ExceptionTypeFilter(errors.UsernameDoesNotExistError)
    )


async def username_does_not_exist_error_handler(event: ErrorEvent) -> None:
    await event.update.message.answer(
        f"<b>Username {event.exception.username} doesn't exist</b>"
    )


async def incorrect_password_error_handler(event: ErrorEvent) -> None:
    await event.update.message.answer("<b>Incorrect password</b>")