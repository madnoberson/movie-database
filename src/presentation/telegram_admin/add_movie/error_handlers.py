from aiogram.types import ErrorEvent


async def invalid_title_error_handler(event: ErrorEvent) -> None:
    await event.update.message.answer("Title is required")


async def invalid_release_date_error_handler(event: ErrorEvent) -> None:
    await event.update.message.answer("Invalid release date")


async def invalid_poster_error_handler(event: ErrorEvent) -> None:
    await event.update.message.answer("Invalid poster")


async def invalid_genres_error_handler(event: ErrorEvent) -> None:
    await event.update.message.answer("Invalid genres")


async def invalid_status_error_handler(event: ErrorEvent) -> None:
    await event.update.message.answer("Invalid status")


async def invalid_mpaa_error_handler(event: ErrorEvent) -> None:
    await event.update.message.answer("Invalid mpaa")