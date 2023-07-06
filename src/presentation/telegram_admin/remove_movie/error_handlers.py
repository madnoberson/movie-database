from aiogram.types import ErrorEvent


async def invalid_movie_id_error_handler(event: ErrorEvent) -> None:
    await event.update.message.answer("Invalid movie id")


async def movie_does_not_exist_error_handler(event: ErrorEvent) -> None:
    movie_id = event.exception.movie_id
    await event.update.message.answer(f"Movie {movie_id} doesn't exist")