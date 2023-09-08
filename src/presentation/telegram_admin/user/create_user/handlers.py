from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import StatesGroup, State

from src.application.interactors.user.create_user.dto import CreateUserDTO
from src.presentation.telegram_admin.common.ioc import TelegramAdminIoC
from . import templates
from . import keyboards


class CreateUserStates(StatesGroup):

    set_email = State()
    set_password = State()
    confirmation = State()
    

async def create_user(message: Message, state: FSMContext) -> None:
    """Entrypoint for `CreateUser` use case dialog"""
    await message.answer(text=templates.set_email())
    await state.set_state(CreateUserStates.set_email)


async def set_email(message: Message, state: FSMContext) -> None:
    """Set email for `CreateUser` use case"""
    await message.answer(text=templates.set_password())
    await state.update_data(email=message.text)
    await state.set_state(CreateUserStates.set_password)


async def set_password(message: Message, state: FSMContext) -> None:
    """Set password for `CreateUser` use case"""
    data = await state.get_data()
    text = templates.confirm(email=data["email"], password=message.text)
    await message.answer(text=text, reply_markup=keyboards.confirm())
    await state.update_data(password=message.text)
    await state.set_state(CreateUserStates.confirmation)


async def confirm(callback: CallbackQuery, ioc: TelegramAdminIoC, state: FSMContext) -> None:
    """Execute of `CreateUser` use case and end the dialog"""
    data = await state.get_data()
    dto = CreateUserDTO(email=data["email"], password=data["password"])
    result = await ioc.create_user(dto)
    text = templates.confirmed(user_id=result.user_id, email=data["email"], password=data["password"])
    await callback.message.edit_text(text=text)
    await callback.answer()
    await state.clear()


async def cancel(callback: CallbackQuery, state: FSMContext) -> None:
    """Cancel preparing for `CreateUser` use case and end the dialog"""
    await callback.message.edit_text(templates.canceled())
    await callback.answer()
    await state.clear()
    
