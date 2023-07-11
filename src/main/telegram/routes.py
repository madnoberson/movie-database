from aiogram import Dispatcher

from src.presentation.telegram.register import creaet_register_router
from src.presentation.telegram.login import create_login_router


def setup_routes(dp: Dispatcher) -> None:
    register_router = creaet_register_router()
    login_router = create_login_router()

    dp.include_routers(
        register_router,
        login_router
    )
