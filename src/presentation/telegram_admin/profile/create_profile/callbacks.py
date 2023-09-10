from aiogram.filters.callback_data import CallbackData


class Confirm(CallbackData, prefix="create_profile_confirm"):

    value: bool