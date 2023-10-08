from aiogram.types.error_event import ErrorEvent

from . import templates


async def user_already_exists(event: ErrorEvent) -> None:
    await event.update.message.answer(text=templates.user_already_exists())