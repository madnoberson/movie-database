from aiogram import Dispatcher

from src.presentation.telegram.routers.auth import create_user_router


def setup_routes(dispatcher: Dispatcher) -> None:
    dispatcher.include_routers(
        create_user_router()
    )