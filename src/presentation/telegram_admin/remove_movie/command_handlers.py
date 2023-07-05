from aiogram.types import Message

from src.application.common.result import Result
from src.application.common.errors.movie import (
    MovieDoesNotExistError
)
from src.presentation.telegram_admin.interactor import (
    TelegramAdminInteractor
)
from src.application.commands.remove_movie.command import (
    RemoveMovieCommand
)
from .validators import validate_movie_id


async def remove_movie_command_handler(
    message: Message,
    interactor: TelegramAdminInteractor
) -> None:
    movie_id = validate_movie_id(message.text)

    command = RemoveMovieCommand(movie_id)
    result = interactor.handle_remove_movie_command(
        command=command
    )

    match result:

        case Result(None, MovieDoesNotExistError() as error):
            await message.answer(f"Movie {movie_id} doesn't exist")
        
        case Result(None, None):
            await message.answer("Movie removed")