from aiogram.fsm.state import StatesGroup, State


class CreateUserStates(StatesGroup):

    set_email = State()
    set_password = State()
    confirmation = State()