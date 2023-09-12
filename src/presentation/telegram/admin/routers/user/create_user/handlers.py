from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from src.application.interactors.user.create_user.dto import CreateUserDTO
from src.application.interactors.user.create_user.interactor import CreateUser
from src.application.interactors.queries.user.check_email_exists.dto import CheckEmailExistsDTO
from src.application.interactors.queries.user.check_email_exists.interactor import CheckEmailExists
from src.presentation.telegram.common.interactor_factory import InteractorFactory
from . import states
from . import templates
from . import keyboards
    

async def create_user(message: Message, state: FSMContext) -> None:
    """Entrypoint for `CreateUser` use case dialog"""
    await message.answer(text=templates.set_email())
    await state.set_state(states.CreateUserStates.set_email)


async def set_email(
    message: Message, state: FSMContext,
    check_email_exists_interactor_factory: InteractorFactory[CheckEmailExists]
) -> None:
    """Sets email for `CreateUser` use case"""
    async with check_email_exists_interactor_factory.create_interactor() as check_email_exists:
        dto = CheckEmailExistsDTO(email=message.text)
        result = await check_email_exists(dto)
    if result.email_exists:
        await message.answer(templates.email_exists())
    else:
        await message.answer(text=templates.set_password())
        await state.update_data(email=message.text)
        await state.set_state(states.CreateUserStates.set_password)


async def set_password(message: Message, state: FSMContext) -> None:
    """Sets password for `CreateUser` use case"""
    data = await state.get_data()
    text = templates.confirm(email=data["email"], password=message.text)
    await message.answer(text=text, reply_markup=keyboards.confirm())
    await state.update_data(password=message.text)
    await state.set_state(states.CreateUserStates.confirmation)


async def confirm(
    callback: CallbackQuery, state: FSMContext,
    create_user_interactor_factory: InteractorFactory[CreateUser]
) -> None:
    """Executes `CreateUser` use case and ends the dialog"""
    async with create_user_interactor_factory.create_interactor() as create_user:
        data = await state.get_data()
        dto = CreateUserDTO(email=data["email"], password=data["password"])
        result = await create_user(dto)
    text = templates.confirmed(
        user_id=result.user_id, email=data["email"], password=data["password"]
    )
    await callback.message.edit_text(text=text, reply_markup=keyboards.create_profile())
    await callback.answer()
    await state.update_data(user_id=result.user_id)
    await state.set_state(None)


async def cancel(callback: CallbackQuery, state: FSMContext) -> None:
    """Cancels preparing for `CreateUser` use case and end the dialog"""
    await callback.message.edit_text(templates.canceled())
    await callback.answer()
    await state.clear()
    
