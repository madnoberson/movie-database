from aiogram import Dispatcher

from app.presentation.telegram.routers.auth import create_auth_router


def setup_routes(dispatcher: Dispatcher) -> None:
    dispatcher.include_routers(create_auth_router())