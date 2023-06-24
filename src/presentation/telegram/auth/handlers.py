from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from src.application.common.result import Result
from src.presentation.interactor import Interactor
from src.application.commands.register.command import (
    RegisterCommand,
    RegisterCommandResult
)
from src.application.commands.register.errors import (
    UsernameAlreadyExistsError
)
from src.application.queries.username_existence.query import (
    CheckUsernameExistenceQuery
)
from .states import Register


auth_router = Router()


@auth_router.message(Command("register"))
async def register_command(
    message: Message,
    state: FSMContext
) -> None:
    user_data = await state.get_data()
    user_id = user_data.get("user_id")

    if user_id:
        await message.answer("Already loged in")
    else:
        await message.answer(text="Set username")
        await state.set_state(Register.set_username)


@auth_router.message(Register.set_username)
async def register_command_set_username(
    message: Message,
    state: FSMContext,
    ioc: Interactor
) -> None:
    # TODO: Validate username

    query = CheckUsernameExistenceQuery(
        username=message.text
    )
    result = ioc.handle_check_username_existence_query(
        query=query
    )
    
    if result.value.exists:
        await message.answer(
            text=f"Username {message.text} already exists"
        )
    else:
        await message.answer("Set password")
        await state.update_data(username=message.text)
        await state.set_state(Register.set_password)
        

@auth_router.message(Register.set_password)
async def register_command_set_password(
    message: Message,
    state: FSMContext,
    ioc: Interactor
) -> None:
    # TODO: Validate password

    user_data = await state.get_data()

    command = RegisterCommand(
        username=user_data["username"],
        password=message.text
    )
    result = ioc.handle_register_command(command)

    match result:

        case Result(None, UsernameAlreadyExistsError()):
            # TODO: Handler server error
            await message.answer("Error 500")

        case Result(RegisterCommandResult(), None):
            await message.answer("Success")
            await state.set_data(
                {"user_id": result.value.user_id.hex}
            )
    
    await state.set_state(None)
