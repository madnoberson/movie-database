from aiogram import Router

from .create_profile import create_create_profile_router


def create_profile_router() -> Router:
    router = Router()

    router.include_router(create_create_profile_router())

    return router