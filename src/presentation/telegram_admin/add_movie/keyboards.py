from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.domain.models.movie.constants import (
    MovieStatusEnum,
    MovieGenreEnum,
    MPAAEnum
)
from .callbacks import (
    SetGenresCallbackFactory,
    SetStatusCallbackFactory,
    SetMpaaCallbackFactory,
    ConfirmCallbackFactory
)


def set_genres(selected: list[MovieGenreEnum] = []) -> InlineKeyboardMarkup:
    """
    Returns inline keyboard markup for
    `add_movie_command_handler_set_genres`
    """

    builder = InlineKeyboardBuilder()
    for enum_field in MovieGenreEnum:

        if enum_field in selected:
            callback_data = SetGenresCallbackFactory(
                action="remove",
                value=enum_field
            )
            builder.button(
                text=f"{enum_field.name.capitalize()} ✅",
                callback_data=callback_data
            )
            continue

        builder.button(
            text=enum_field.name.capitalize(),
            callback_data=SetGenresCallbackFactory(value=enum_field)
        )

    builder.button(
        text="Done ✅",
        callback_data=SetGenresCallbackFactory(action="done", value=None)
    )
    builder.adjust(2)
    
    return builder.as_markup()


def set_status() -> InlineKeyboardMarkup:
    """
    Returns inline keyboard markup for
    `add_movie_command_handler_set_status`
    """

    builder = InlineKeyboardBuilder()
    for enum_field in MovieStatusEnum:
        builder.button(
            text=enum_field.name.capitalize(),
            callback_data=SetStatusCallbackFactory(value=enum_field)
        )
    
    builder.adjust(3)
    builder.button(
        text="Skip",
        callback_data=SetStatusCallbackFactory(value=None)
    )

    return builder.as_markup()


def set_mpaa() -> InlineKeyboardMarkup:
    """
    Returns inline keyboard markup for
    `add_movie_command_handler_set_mpaa`
    """

    builder = InlineKeyboardBuilder()
    for enum_field in MPAAEnum:
        builder.button(
            text=enum_field.name.capitalize(),
            callback_data=SetMpaaCallbackFactory(value=enum_field)
        )
    
    builder.button(
        text="Skip",
        callback_data=SetMpaaCallbackFactory(value=None)
    )
    builder.adjust(5)
    

    return builder.as_markup()


def confirm() -> InlineKeyboardMarkup:
    """
    Returns inline keyboard markup for
    `add_movie_command_handler_confirm`
    """

    builder = InlineKeyboardBuilder()

    builder.button(
        text="Cancel 🚫",
        callback_data=ConfirmCallbackFactory(confirm=False)
    )
    builder.button(
        text="Confirm ✅",
        callback_data=ConfirmCallbackFactory(confirm=True)
    )

    return builder.as_markup()


