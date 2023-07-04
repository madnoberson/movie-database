from aiogram import Router
from aiogram.filters import Command, ExceptionTypeFilter

from .command_handlers import (
    add_movie_command_handler,
    add_movie_command_handler_set_title,
    add_movie_command_handler_set_release_date,
    add_movie_command_handler_set_poster,
    add_movie_command_handler_set_genres,
    add_movie_command_handler_set_status,
    add_movie_command_handler_set_mpaa
)
from .error_handlers import (
    invalid_title_error_handler,
    invalid_release_date_error_handler,
    invalid_poster_error_handler,
    invalid_genres_error_handler,
    invalid_status_error_handler,
    invalid_mpaa_error_handler
)
from .errors import (
    InvalidTitleError,
    InvalidReleaseDateError,
    InvalidPosterError,
    InvalidGenresError,
    InvalidStatusError,
    InvalidMpaaError
)
from .states import AddMovieStatesGroup


__all__ = ("create_add_movie_router",)


def setup_command_handlers(router: Router) -> None:
    router.message.register(
        add_movie_command_handler,
        Command("add_movie")
    )
    router.message.register(
        add_movie_command_handler_set_title,
        AddMovieStatesGroup.set_title
    )
    router.message.register(
        add_movie_command_handler_set_release_date,
        AddMovieStatesGroup.set_release_date
    )
    router.message.register(
        add_movie_command_handler_set_poster,
        AddMovieStatesGroup.set_poster
    )
    router.message.register(
        add_movie_command_handler_set_genres,
        AddMovieStatesGroup.set_genres
    )
    router.message.register(
        add_movie_command_handler_set_status,
        AddMovieStatesGroup.set_status
    )
    router.message.register(
        add_movie_command_handler_set_mpaa,
        AddMovieStatesGroup.set_mpaa
    )


def setup_error_handlers(router: Router) -> None:
    router.errors.register(
        invalid_title_error_handler,
        ExceptionTypeFilter(InvalidTitleError)
    )
    router.errors.register(
        invalid_release_date_error_handler,
        ExceptionTypeFilter(InvalidReleaseDateError)
    )
    router.errors.register(
        invalid_poster_error_handler,
        ExceptionTypeFilter(InvalidPosterError)
    )
    router.errors.register(
        invalid_genres_error_handler,
        ExceptionTypeFilter(InvalidGenresError)
    )
    router.errors.register(
        invalid_status_error_handler,
        ExceptionTypeFilter(InvalidStatusError)
    )
    router.errors.register(
        invalid_mpaa_error_handler,
        ExceptionTypeFilter(InvalidMpaaError)
    )
    

def create_add_movie_router() -> Router:
    add_movie_router = Router()

    setup_command_handlers(add_movie_router)
    setup_error_handlers(add_movie_router)

    return add_movie_router