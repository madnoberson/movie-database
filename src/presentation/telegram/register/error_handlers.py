from aiogram import Router
from aiogram.types.error_event import ErrorEvent
from aiogram.filters.exception import ExceptionTypeFilter

from src.application.commands.register.errors import UsernameAlreadyExistsError
from . import templates


__all__ = ("setup_error_handlers",)


def setup_error_handlers(router: Router) -> None:
    router.errors.register(
        username_already_exists_error_handler,
        ExceptionTypeFilter(UsernameAlreadyExistsError)
    )


async def username_already_exists_error_handler(event: ErrorEvent) -> None:
    message_text = templates.username_exists(event.exception.username)
    await event.update.message.answer(message_text)