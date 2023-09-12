from aiogram.filters.callback_data import CallbackData


class Confirm(CallbackData, prefix="create_user_confirm"):

    value: bool