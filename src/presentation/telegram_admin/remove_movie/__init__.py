from aiogram import Router
from aiogram.filters import Command, ExceptionTypeFilter

from src.application.common.errors.movie import MovieDoesNotExistError
from .command_handlers import (
    remove_movie_command_handler,
    remove_movie_command_handler_set_movie_id,
    remove_movie_command_handler_confirm
)
from .error_handlers import (
    invalid_movie_id_error_handler,
    movie_does_not_exist_error_handler
)
from .errors import InvalidMovieIdError
from .states import RemoveMovieStatesGroup


def setup_command_handlers(router: Router) -> None:
    router.message.register(
        remove_movie_command_handler,
        Command("remove_movie")
    )
    router.message.register(
        remove_movie_command_handler_set_movie_id,
        RemoveMovieStatesGroup.set_movie_id
    )
    router.message.register(
        remove_movie_command_handler_confirm,
        RemoveMovieStatesGroup.confirm
    )


def setup_error_handlers(router: Router) -> None:
    router.errors.register(
        invalid_movie_id_error_handler,
        ExceptionTypeFilter(InvalidMovieIdError)
    )
    router.errors.register(
        movie_does_not_exist_error_handler,
        MovieDoesNotExistError
    )


def create_remove_movie_router() -> Router:
    remove_movie_router = Router()

    setup_command_handlers(remove_movie_router)
    setup_error_handlers(remove_movie_router)

    return remove_movie_router