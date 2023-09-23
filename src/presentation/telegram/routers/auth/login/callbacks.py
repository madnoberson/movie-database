from aiogram.filters.callback_data import CallbackData


class Login(CallbackData, prefix="confirm_login"):

    value: bool