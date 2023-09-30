from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from . import callbacks


def confirm() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(
        text="Cancel 🚫",
        callback_data=callbacks.Confirm(value=False)
    )
    builder.button(
        text="Confirm ✅",
        callback_data=callbacks.Confirm(value=True)
    )

    return builder.as_markup()