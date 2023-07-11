from aiogram import Dispatcher
from aiogram.types.error_event import ErrorEvent
from aiogram.filters.exception import ExceptionTypeFilter

from . import errors


__all__ = ("setup_error_handlers",)


def setup_error_handlers(dp: Dispatcher) -> None:
    dp.errors.register(
        invalid_password_error_handler,
        ExceptionTypeFilter(errors.InvalidPassword)
    )


async def invalid_password_error_handler(event: ErrorEvent) -> None:
    await event.update.message.answer(event.exception.messsage)