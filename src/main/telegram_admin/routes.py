from aiogram import Dispatcher

from src.presentation.telegram_admin.add_movie import create_add_movie_router


def setup_routes(dp: Dispatcher) -> None:
    add_movie_router = create_add_movie_router()
    dp.include_router(add_movie_router)
