from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.presentation.telegram.admin.common.callbacks import CreateProfile
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


def create_profile() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(
        text="Create a profile for this user",
        callback_data=CreateProfile()
    )

    return builder.as_markup()