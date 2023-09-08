from aiogram.filters.callback_data import CallbackData


class ConfirmCallbackData(CallbackData, prefix="create_user_confirm"):

    value: bool