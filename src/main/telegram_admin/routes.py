from aiogram import Dispatcher

from src.presentation.telegram_admin.user import create_user_router


def setup_routes(dispatcher: Dispatcher) -> None:
    dispatcher.include_routers(create_user_router())