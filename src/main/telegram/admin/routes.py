from aiogram import Dispatcher

from src.presentation.telegram.admin.routers.user import create_user_router
from src.presentation.telegram.admin.routers.profile import create_profile_router


def setup_routes(dispatcher: Dispatcher) -> None:
    dispatcher.include_routers(
        create_user_router(), create_profile_router()
    )