from aiogram import Router

from .create_user import create_create_user_router


def create_user_router() -> Router:
    router = Router()

    router.include_router(create_create_user_router())

    return router