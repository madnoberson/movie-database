from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from src.presentation.telegram.interactor import TelegramInteractor
from src.application.queries.username_existence.query import CheckUsernameExistenceQuery
from src.application.commands.register.command import RegisterCommand
from src.presentation.telegram.common.errors import InvalidPassword
from . import templates


__all__ = ("setup_handlers",)


def setup_handlers(router: Router) -> None:
    router.message.register(
        register_command_handler,
        Command("register")
    )
    router.message.register(
        register_command_handler_set_username,
        RegisterStatesGroup.set_username
    )
    router.message.register(
        register_command_handler_set_password,
        RegisterStatesGroup.set_password
    )


class RegisterStatesGroup(StatesGroup):

    set_username = State()
    set_password = State()


async def register_command_handler(
    message: Message,
    state: FSMContext
) -> None:
    await message.answer(templates.set_username())
    await state.set_state(RegisterStatesGroup.set_username)


async def register_command_handler_set_username(
    message: Message,
    state: FSMContext,
    interactor: TelegramInteractor
) -> None:
    if (username := message.text) is None or message.text == "_":
        username = message.from_user.username
    
    query = CheckUsernameExistenceQuery(username)
    res = interactor.handle_check_username_existence_query(query)

    if res.exists:
        await message.answer()
    else:
        await state.update_data(username=username)
        await message.answer(templates.set_password())
        await state.set_state(RegisterStatesGroup.set_password)


async def register_command_handler_set_password(
    message: Message,
    state: FSMContext,
    interactor: TelegramInteractor
) -> None:
    if (password := message.text) is None:
        raise InvalidPassword()
    
    state_data = await state.get_data()
    command = RegisterCommand(
        username=state_data.get("username"),
        password=password
    )
    interactor.handle_register_command(command)

    await message.answer(templates.successfully_registred())
    await state.clear()




