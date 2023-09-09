from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from . import states
from . import templates


async def create_profile(callback: CallbackQuery, state: FSMContext) -> None:
    """Entrypoint for `CreateProfile` use case dialog"""
    await callback.message.answer(text=templates.set_username())
    await state.set_state(states.CreateProfileStates.set_username)


async def set_username(message: Message, state: FSMContext) -> None:
    """Set username for `CreateProfile` use case"""
    ...


async def confirm(callback: CallbackQuery, state: FSMContext) -> None:
    ...
    
