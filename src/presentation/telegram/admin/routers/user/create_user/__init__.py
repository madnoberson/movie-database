from aiogram import Router, F
from aiogram.filters import Command

from . import states
from . import handlers
from . import filters
from . import callbacks


__all__ = ["create_create_user_router"]


def create_create_user_router() -> Router:
    router = Router()

    setup_handlers(router)

    return router


def setup_handlers(router: Router) -> None:
    router.message.register(handlers.create_user, Command("create_user"))
    router.message.register(handlers.set_email, states.CreateUserStates.set_email, filters.email)
    router.message.register(handlers.set_password, states.CreateUserStates.set_password, filters.password)
    router.callback_query.register(handlers.confirm, callbacks.Confirm.filter(F.value == True))
    router.callback_query.register(handlers.cancel, callbacks.Confirm.filter(F.value == False))
    