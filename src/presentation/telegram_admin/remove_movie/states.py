from aiogram.fsm.state import StatesGroup, State


class RemoveMovieStatesGroup(StatesGroup):

    set_movie_id = State()
    
    confirm = State()