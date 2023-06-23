from aiogram import Router
from aiogram.filters import Command, CommandObject
from aiogram.types import Message

from src.application.common.result import Result
from src.presentation.interactor import Interactor
from src.application.commands.register.command import (
    RegisterCommand,
    RegisterCommandResult
)
from src.application.commands.register.errors import (
    UsernameAlreadyExistsError
)


auth_router = Router()


@auth_router.message(Command("register"))
async def register_command(
    message: Message,
    command: CommandObject,
    ioc: Interactor
) -> None:
    args = command.args or [] 
    username, password = args.split()

    command = RegisterCommand(
        username=username,
        password=password
    )
    result = ioc.handle_register_command(
        command=command
    )

    match result:

        case Result(RegisterCommandResult(), None):
            await message.answer(f"{username} {password}")
        
        case Result(None, UsernameAlreadyExistsError()):
            text = f"Username {result.error.username} already exists"
            await message.answer(text)
