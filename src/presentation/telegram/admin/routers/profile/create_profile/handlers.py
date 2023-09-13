from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from src.application.interactors.profile.create_profile.dto import CreateProfileDTO
from src.application.interactors.profile.create_profile.interactor import CreateProfile
from src.application.interactors.queries.profile.check_username_exists.dto import CheckUsernameExistsDTO
from src.application.interactors.queries.profile.check_username_exists.interactor import CheckUsernameExists
from src.presentation.telegram.common.interactor_factory import InteractorFactory
from . import states
from . import templates
from . import keyboards


async def create_profile(callback: CallbackQuery, state: FSMContext) -> None:
    """Entrypoint for `CreateProfile` use case dialog"""
    await callback.message.answer(text=templates.set_username())
    await state.set_state(states.CreateProfileStates.set_username)


async def set_username(
    message: Message, state: FSMContext,
    check_username_exists_interactor_factory: InteractorFactory[CheckUsernameExists]
) -> None:
    """Sets username for `CreateProfile` use case"""
    async with check_username_exists_interactor_factory.create_interactor() as check_username_exists:
        dto = CheckUsernameExistsDTO(username=message.text)
        result = await check_username_exists(dto)
    if result["username_exists"]:
        await message.answer(templates.username_exists())
    else:
        data = await state.get_data()
        text = templates.confirm(user_id=data["user_id"], username=message.text)
        await message.answer(text=text, reply_markup=keyboards.confirm())
        await state.update_data(username=message.text)
        await state.set_state(states.CreateProfileStates.confirmation)


async def confirm(
    callback: CallbackQuery, state: FSMContext,
    create_profile_interactor_factory: InteractorFactory[CreateProfile]
) -> None:
    """Executes `CreateProfile` use case and ends the dialog"""
    async with create_profile_interactor_factory.create_interactor() as create_profile:
        data = await state.get_data()
        dto = CreateProfileDTO(user_id=data["user_id"], username=data["username"])
        result = await create_profile(dto)
    text = templates.confirmed(
        user_id=data["user_id"], profile_id=result.profile_id, username=data["username"]
    )
    await callback.message.edit_text(text=text)
    await callback.answer()
    await state.clear()


async def cancel(callback: CallbackQuery, state: FSMContext) -> None:
    """Cancels preparing for `CreateUser` use case and end the dialog"""
    await callback.message.edit_text(templates.canceled())
    await callback.answer()
    await state.clear()
    
