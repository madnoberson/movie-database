from aiogram import Dispatcher

from src.presentation.telegram_admin.add_movie import create_add_movie_router
from src.presentation.telegram_admin.remove_movie import create_remove_movie_router


def setup_routes(dp: Dispatcher) -> None:
    add_movie_router = create_add_movie_router()
    dp.include_router(add_movie_router)

    remove_movie_router = create_remove_movie_router()
    dp.include_router(remove_movie_router)