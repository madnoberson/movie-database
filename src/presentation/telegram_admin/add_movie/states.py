from aiogram.fsm.state import StatesGroup, State


class AddMovieStatesGroup(StatesGroup):

    set_title = State()
    set_release_date = State()
    set_poster = State()
    set_status = State()
    set_genres = State()
    set_mpaa = State()
