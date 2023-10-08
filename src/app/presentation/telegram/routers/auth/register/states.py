from aiogram.fsm.state import StatesGroup, State


class Register(StatesGroup):

    set_username = State()
    set_password = State()
    confirm = State()