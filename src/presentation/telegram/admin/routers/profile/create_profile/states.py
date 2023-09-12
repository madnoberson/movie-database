from aiogram.fsm.state import StatesGroup, State


class CreateProfileStates(StatesGroup):

    set_username = State()
    confirmation = State()