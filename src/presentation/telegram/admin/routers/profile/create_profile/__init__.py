from aiogram import Router, F

from src.presentation.telegram.admin.common.callbacks import CreateProfile
from . import states
from . import handlers
from . import filters
from . import callbacks


__all__ = ["create_create_profile_router"]


def create_create_profile_router() -> Router:
    router = Router()

    setup_handlers(router)

    return router


def setup_handlers(router: Router) -> None:
    router.callback_query.register(handlers.create_profile, CreateProfile.filter())
    router.message.register(handlers.set_username, states.CreateProfileStates.set_username, filters.username)
    router.callback_query.register(handlers.confirm, callbacks.Confirm.filter(F.value == True))
    router.callback_query.register(handlers.cancel, callbacks.Confirm.filter(F.value == False))