from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from . import templates
from . import errors


__all__ = ("setup_handlers",)


def setup_handlers(router: Router) -> None:
    router.message.register(
        whoami_command_handler,
        Command("whoami")
    )
    router.message.register(
        logout_command_handler,
        Command("logout")
    )


async def whoami_command_handler(
    message: Message,
    state: FSMContext
) -> None:
    state_data = await state.get_data()
    user_id = state_data.get("user_id")

    if user_id is None:
        raise errors.UserIsNotLogedIn()
    
    username = state_data.get("username")
    await message.answer(templates.whoami(user_id, username))


async def logout_command_handler(
    message: Message,
    state: FSMContext
) -> None:
    state_data = await state.get_data()

    if state_data.get("user_id") is None:
        raise errors.UserIsNotLogedIn()

    await state.clear()
    await message.answer(templates.logout())
