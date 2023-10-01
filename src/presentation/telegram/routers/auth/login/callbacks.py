from aiogram.filters.callback_data import CallbackData


class Confirm(CallbackData, prefix="confirm_login"):

    value: bool