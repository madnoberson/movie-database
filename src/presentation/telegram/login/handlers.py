from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from src.presentation.telegram.interactor import TelegramInteractor
from src.application.queries.login.query import LoginQuery
from . import templates


def setup_handlers(router: Router) -> None:
    router.message.register(
        login_command_handler,
        Command("login")
    )


class LoginStatesGroup(StatesGroup):

    enter_username = State()
    enter_password = State()


async def login_command_handler(
    message: Message,
    state: FSMContext
) -> None:
    await message.answer(templates.enter_username())
    await state.set_state(LoginStatesGroup.enter_username)


async def login_command_handler_enter_username(
    message: Message,
    state: FSMContext
) -> None:
    if username := message.text is None or username == "_":
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
        ...
    
    state_data = await state.get_data()
    query = LoginQuery(
        username=state_data.get("username"),
        password=password
    )
    interactor.handler_login_query(query)

    await message.answer("Successfully loged in")
    await state.clear()