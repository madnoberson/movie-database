from aiogram import Dispatcher

from src.presentation.telegram.common import create_common_router
from src.presentation.telegram.register import creaet_register_router
from src.presentation.telegram.login import create_login_router


def setup_routes(dp: Dispatcher) -> None:
    common_router = create_common_router()
    register_router = creaet_register_router()
    login_router = create_login_router()

    dp.include_routers(
        common_router,
        register_router,
        login_router
    )
