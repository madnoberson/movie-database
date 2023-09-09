from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from src.application.interactors.user.create_user.dto import CreateUserDTO
from src.application.interactors.queries.user.check_email_exists.dto import CheckEmailExistsDTO
from src.presentation.telegram_admin.common.ioc import TelegramAdminIoC
from . import states
from . import templates
from . import keyboards
    

async def create_user(message: Message, state: FSMContext) -> None:
    """Entrypoint for `CreateUser` use case dialog"""
    await message.answer(text=templates.set_email())
    await state.set_state(states.CreateUserStates.set_email)


async def set_email(message: Message, ioc: TelegramAdminIoC, state: FSMContext) -> None:
    """Set email for `CreateUser` use case"""
    data = CheckEmailExistsDTO(email=message.text)
    result = await ioc.check_email_exists(data)
    if result.email_exists:
        await message.answer(templates.email_exists())
    else:
        await message.answer(text=templates.set_password())
        await state.update_data(email=message.text)
        await state.set_state(states.CreateUserStates.set_password)


async def set_password(message: Message, state: FSMContext) -> None:
    """Set password for `CreateUser` use case"""
    data = await state.get_data()
    text = templates.confirm(email=data["email"], password=message.text)
    await message.answer(text=text, reply_markup=keyboards.confirm())
    await state.update_data(password=message.text)
    await state.set_state(states.CreateUserStates.confirmation)


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
    
