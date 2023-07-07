from fastapi import FastAPI, Request
from fastapi.responses import ORJSONResponse

from src.application.common.errors.movie import MovieDoesNotExistError
from src.application.common.errors.user import UserDoesNotExistError
from src.application.common.errors.user_movie_rating import UserMovieRatingDoesNotExistError
from src.application.commands.rate_movie.errors import UserMovieRatingAlreadyExistsError
from src.application.commands.register.errors import UsernameAlreadyExistsError
from src.application.queries.login.errors import UsernameDoesNotExistError, PasswordIsIncorrectError


def setup_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(
        MovieDoesNotExistError,
        movie_does_not_exist_error_handler
    )
    app.add_exception_handler(
        UserDoesNotExistError,
        user_does_not_exist_error_handler
    )
    app.add_exception_handler(
        UserMovieRatingDoesNotExistError,
        user_movie_rating_does_not_exist_error_handler
    )
    app.add_exception_handler(
        UserMovieRatingAlreadyExistsError,
        user_movie_rating_already_exists_error_handler
    )
    app.add_exception_handler(
        UsernameAlreadyExistsError,
        username_already_exists_error_handler
    )
    app.add_exception_handler(
        UsernameDoesNotExistError,
        username_does_not_exist_error_handler
    )
    app.add_exception_handler(
        PasswordIsIncorrectError,
        incorrect_password_error_handler
    )


def movie_does_not_exist_error_handler(
    request: Request,
    error: MovieDoesNotExistError
) -> ORJSONResponse:
    return ORJSONResponse(
        content={"message": error.message},
        status_code=404
    )


def user_does_not_exist_error_handler(
    request: Request,
    error: UserDoesNotExistError
) -> ORJSONResponse:
    return ORJSONResponse(
        content={"message": error.message},
        status_code=401
    )


def user_movie_rating_does_not_exist_error_handler(
    request: Request,
    error: UserMovieRatingDoesNotExistError
) -> ORJSONResponse:
    return ORJSONResponse(
        content={"message": error.message},
        status_code=404
    )


def user_movie_rating_already_exists_error_handler(
    request: Request,
    error: UserMovieRatingAlreadyExistsError
) -> ORJSONResponse:
    return ORJSONResponse(
        content={"message": error.message},
        status_code=409
    )


def username_already_exists_error_handler(
    request: Request,
    error: UsernameAlreadyExistsError
) -> ORJSONResponse:
    return ORJSONResponse(
        content={"message": error.message},
        status_code=409
    )


def username_does_not_exist_error_handler(
    request: Request,
    error: UsernameDoesNotExistError
) -> ORJSONResponse:
    return ORJSONResponse(
        content={"message": error.message},
        status_code=404
    )


def incorrect_password_error_handler(
    request: Request,
    error: PasswordIsIncorrectError
) -> ORJSONResponse:
    return ORJSONResponse(
        content={"message": error.message},
        status_code=401
    )
