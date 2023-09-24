from aiogram import Router, F
from aiogram.filters import Command

from . import states
from . import filters
from . import handlers
from . import callbacks


def create_register_router() -> Router:
    router = Router()

    setup_handlers(router)

    return router


def setup_handlers(router: Router) -> None:
    router.message.register(handlers.register, Command("register"))
    router.message.register(handlers.set_username, states.Register.set_username, filters.username)
    router.message.register(handlers.set_password, states.Register.set_password, filters.password)
    router.callback_query.register(handlers.confirm, callbacks.Confirm.filter(F.value == True))
    router.callback_query.register(handlers.cancel, callbacks.Confirm.filter(F.value == False))