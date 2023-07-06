from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from .states import AddMovieStatesGroup
from .validators import (
    validate_title,
    validate_release_date,
    validate_poster,
    validate_genres,
    validate_status,
    validate_mpaa
)


async def add_movie_command_handler(
    message: Message,
    state: FSMContext
) -> None:
    await message.answer("Set title")
    await state.set_state(AddMovieStatesGroup.set_title)


async def add_movie_command_handler_set_title(
    message: Message,
    state: FSMContext
) -> None:
    title = validate_title(message.text)
    await state.update_data(title=title)

    await message.answer("Set release date")
    await state.set_state(AddMovieStatesGroup.set_release_date)


async def add_movie_command_handler_set_release_date(
    message: Message,
    state: FSMContext
) -> None:
    release_date = validate_release_date(message.text)
    await state.update_data(release_date=release_date)

    await message.answer("Set poster (Optionaly)")
    await state.set_state(AddMovieStatesGroup.set_poster)


async def add_movie_command_handler_set_poster(
    message: Message,
    state: FSMContext
) -> None:
    poster = validate_poster(message.photo)
    await state.update_data(poster=poster)

    await message.answer("Set genres (Optionaly)")
    await state.set_state(AddMovieStatesGroup.set_genres)


async def add_movie_command_handler_set_genres(
    message: Message,
    state: FSMContext
) -> None:
    genres = validate_genres(message.text)
    await state.update_data(genres=genres)
    
    await message.answer("Set status (Optionaly)")
    await state.set_state(AddMovieStatesGroup.set_status)


async def add_movie_command_handler_set_status(
    message: Message,
    state: FSMContext
) -> None:
    status = validate_status(message.text)
    await state.update_data(status=status)

    await message.answer("Set mpaa (Optionaly)")
    await state.set_state(AddMovieStatesGroup.set_mpaa)


async def add_movie_command_handler_set_mpaa(
    message: Message,
    state: FSMContext
) -> None:
    mpaa = validate_mpaa(message.text)
    await state.update_data(mpaa=mpaa)

    await message.answer("Are you sure?")
    await state.set_state(AddMovieStatesGroup.confirm)

    
async def add_movie_command_handler_confirm(
    message: Message,
    state: FSMContext
) -> None:
    ...
