from aiogram import Router
from aiogram.filters import Command, ExceptionTypeFilter

from .command_handlers import remove_movie_command_handler
from .error_handlers import invalid_movie_id_error_handler
from .errors import InvalidMovieIdError


def setup_command_handlers(router: Router) -> None:
    router.message.register(
        remove_movie_command_handler,
        Command("remove_movie")
    )


def setup_error_handlers(router: Router) -> None:
    router.errors.register(
        invalid_movie_id_error_handler,
        ExceptionTypeFilter(InvalidMovieIdError)
    )


def create_remove_movie_router() -> Router:
    remove_movie_router = Router()

    setup_command_handlers(remove_movie_router)
    setup_error_handlers(remove_movie_router)

    return remove_movie_router