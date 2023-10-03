from aiogram.types.error_event import ErrorEvent

from . import templates


async def user_does_not_exist(event: ErrorEvent) -> None:
    await event.update.message.answer(text=templates.user_does_not_exist())


async def user_password_is_not_correct(event: ErrorEvent) -> None:
    await event.update.message.answer(text=templates.user_password_is_not_correct())