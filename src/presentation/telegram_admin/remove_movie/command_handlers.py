from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from src.presentation.telegram_admin.interactor import TelegramAdminInteractor
from src.application.commands.remove_movie.command import RemoveMovieCommand
from .states import RemoveMovieStatesGroup
from .validators import validate_movie_id


async def remove_movie_command_handler(
    message: Message,
    state: FSMContext
) -> None:
    await message.answer("Enter id of the movie that should be removed")
    await state.set_state(RemoveMovieStatesGroup.set_movie_id)


async def remove_movie_command_handler_set_movie_id(
    message: Message,
    state: FSMContext
) -> None:
    movie_id = validate_movie_id(message.text)

    await state.update_data(movie_id=movie_id)
    await state.set_state(RemoveMovieStatesGroup.confirm)


async def remove_movie_command_handler_confirm(
    message: Message,
    state: FSMContext,
    interactor: TelegramAdminInteractor
) -> None:
    state_data = await state.get_data()
    movie_id = state_data.get("movie_id")

    command = RemoveMovieCommand(movie_id)
    interactor.handle_remove_movie_command(command)

    await message.answer("Movie has been successfully removed")
    await state.set_state(None)
            