from aiogram import Router

from .register import create_register_router
from .login import create_login_router


def create_auth_router() -> Router:
    router = Router()

    router.include_routers(
        create_register_router(), create_login_router()
    )

    return router