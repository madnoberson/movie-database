from aiogram import Router, F
from aiogram.filters import Command
from aiogram.filters.exception import ExceptionTypeFilter

from src.application.common.exceptions.user import UserDoesNotExistError, UserPasswordIsNotCorrectError
from . import states
from . import filters
from . import handlers
from . import callbacks
from . import exceptions


def create_login_router() -> Router:
    router = Router()

    setup_handlers(router)
    setup_exception_handlers(router)

    return router


def setup_handlers(router: Router) -> None:
    router.message.register(handlers.login, Command("login"))
    router.message.register(handlers.set_username, states.Login.set_username, filters.username)
    router.message.register(handlers.set_password, states.Login.set_password, filters.password)
    router.callback_query.register(handlers.confirm, callbacks.Confirm.filter(F.value == True))
    router.callback_query.register(handlers.cancel, callbacks.Confirm.filter(F.value == False))


def setup_exception_handlers(router: Router) -> None:
    router.error.register(exceptions.user_does_not_exist, ExceptionTypeFilter(UserDoesNotExistError))
    router.error.register(exceptions.user_password_is_not_correct, ExceptionTypeFilter(UserPasswordIsNotCorrectError))