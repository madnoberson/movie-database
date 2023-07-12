from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from src.presentation.telegram.common.errors import InvalidPasswordError, UserIsAlreadyLoggedIn
from src.presentation.telegram.interactor import TelegramInteractor
from src.application.queries.login.query import LoginQuery
from . import templates


__all__ = ("setup_handlers",)


def setup_handlers(router: Router) -> None:
    router.message.register(
        login_command_handler,
        Command("login")
    )
    router.message.register(
        login_command_handler_enter_username,
        LoginStatesGroup.enter_username
    )
    router.message.register(
        login_command_handler_enter_password,
        LoginStatesGroup.enter_password
    )


class LoginStatesGroup(StatesGroup):

    enter_username = State()
    enter_password = State()


async def login_command_handler(
    message: Message,
    state: FSMContext
) -> None:
    state_data = await state.get_data()
    if state_data.get("user_id") is not None:
        raise UserIsAlreadyLoggedIn()
    
    await message.answer(templates.enter_username())
    await state.set_state(LoginStatesGroup.enter_username)


async def login_command_handler_enter_username(
    message: Message,
    state: FSMContext
) -> None:
    if username := message.text is None or message.text == "_":
        username = message.from_user.username
    
    await state.update_data(username=username)
    await message.answer(templates.enter_password())
    await state.set_state(LoginStatesGroup.enter_password)


async def login_command_handler_enter_password(
    message: Message,
    state: FSMContext,
    interactor: TelegramInteractor
) -> None:
    if password := message.text is None:
        raise InvalidPasswordError()
    
    state_data = await state.get_data()
    query = LoginQuery(
        username=state_data.get("username"),
        password=password
    )
    res = interactor.handle_login_query(query)

    await state.update_data(user_id=res.user_id.hex, password=None)
    await message.answer(templates.successfully_loged_in())
    await state.set_state(None)