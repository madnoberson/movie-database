from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from src.application.queries.auth.login.dto import LoginDTO
from src.application.queries.auth.login.handler import Login
from src.presentation.telegram.common.handler_factory import HandlerFactory
from . import states
from . import templates
from . import keyboards


async def login(message: Message, state: FSMContext):
    """Dialog entry point for `Login` query handler excecuiton"""
    await message.answer(text=templates.set_username())
    await state.set_state(states.Login.set_username)


async def set_username(message: Message, state: FSMContext):
    await message.answer(text=templates.set_password)
    await state.update_data(username=message.text)
    await state.set_state(states.Login.set_password)


async def set_password(message: Message, state: FSMContext):
    text = templates.confirm(
        username=(await state.get_data())["username"],
        password=message.text
    )
    await message.answer(text=text, reply_markup=keyboards.confirm())
    await state.update_data(password=message.text)
    await state.set_state(states.Login.confirm)


async def confirm(
    callback: CallbackQuery, state: FSMContext, login_factory: HandlerFactory[Login]
):
    async with login_factory.create_handler() as login:
        data = await state.get_data()
        dto = LoginDTO(username=data["username"], password=data["password"])
        result = await login(dto)
    await callback.message.edit_text(templates.confirmed())
    await state.clear()
    await state.update_data(current_user_id=result["user_id"])
    await callback.answer()


async def cancel(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text=templates.canceled())
    await callback.answer()
    await state.clear()