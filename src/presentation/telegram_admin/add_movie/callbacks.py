from aiogram.filters.callback_data import CallbackData

from src.domain.models.movie.constants import (
    MovieStatusEnum,
    MovieGenreEnum,
    MPAAEnum
)


class SetGenresCallbackFactory(
    CallbackData,
    prefix="set_genres"
):
    action: str = "add"
    value: MovieGenreEnum | None


class SetStatusCallbackFactory(
    CallbackData,
    prefix="set_status"
):
    value: MovieStatusEnum | None


class SetMpaaCallbackFactory(
    CallbackData,
    prefix="set_mpaa"
):
    value: MPAAEnum | None


class ConfirmCallbackFactory(
    CallbackData,
    prefix="add_movie"
):
    confirm: bool