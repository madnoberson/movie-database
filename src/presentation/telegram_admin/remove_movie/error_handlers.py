from aiogram.types import ErrorEvent


async def invalid_movie_id_error_handler(event: ErrorEvent) -> None:
    await event.update.message.answer("Invalid movie id")