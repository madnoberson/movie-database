from aiogram.types import (
    Message,
    ReplyKeyboardMarkup,
    InlineKeyboardMarkup,
    ReplyKeyboardRemove, 
    ForceReply
)
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State


ReplyMarkup = (
    ReplyKeyboardMarkup |
    InlineKeyboardMarkup | 
    ReplyKeyboardRemove |
    ForceReply
)


async def next_state(
    message: Message,
    state: FSMContext,
    next_state: State,
    text: str,
    text_parse_mode: ParseMode | None = None,
    reply_markup: ReplyMarkup | None = None,
    **state_data
) -> None:
    await state.update_data(**state_data)
    await message.answer(
        text=text,
        parse_mode=text_parse_mode,
        reply_markup=reply_markup
    )
    await state.set_state(next_state)