from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from src.application.interactors.registration.register.dto import RegisterDTO
from src.application.interactors.registration.register.interactor import Register
from src.application.queries.user.check_username_exists.dto import CheckUsernameExistsDTO
from src.application.queries.user.check_username_exists.handler import CheckUsernameExists
from src.presentation.telegram.common.handler_factory import HandlerFactory
from . import states
from . import templates
from . import keyboards


async def register(message: Message, state: FSMContext):
    """Dialog entry point for `Register` use case execution"""
    await message.answer(text=templates.set_username())
    await state.set_state(states.Register.set_username)


async def set_username(
    message: Message, state: FSMContext,
    check_username_exists_factory: HandlerFactory[CheckUsernameExists]
):
    async with check_username_exists_factory.create_handler() as check_username_exists:
        dto = CheckUsernameExistsDTO(username=message.text)
        result = await check_username_exists(dto)
    if result["username_exists"]:
        await message.answer(text=templates.username_already_exists())
        return
    await message.answer(text=templates.set_password())
    await state.update_data(username=message.text)
    await state.set_state(states.Register.set_password)


async def set_password(message: Message, state: FSMContext):
    text = templates.confirm((await state.get_data())["username"])
    await message.answer(text=text, reply_markup=keyboards.confirm())
    await state.set_data(password=message.text)
    await state.set_state(states.Register.confirm)


async def confirm(
    callback: CallbackQuery, state: FSMContext, register_factory: HandlerFactory[Register]
):
    async with register_factory.create_handler() as register:
        data = await state.get_data()
        dto = RegisterDTO(username=data["username"], password=data["password"])
        result = await register(dto)
    await callback.message.edit_text(text=templates.confirmed())
    await state.clear()
    await state.update_data(current_user_id=result.user_id)
    await callback.answer()


async def cancel(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text=templates.canceled())
    await callback.answer()
    await state.clear()