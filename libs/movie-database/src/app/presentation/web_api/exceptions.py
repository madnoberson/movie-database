from typing import Callable, Any

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.application.common.exceptions import auth as auth_exceptions
from app.application.common.exceptions import user as user_exceptions
from app.application.common.exceptions import movie as movie_exceptions
from app.application.common.exceptions import movie_rating as movie_rating_exceptions
from app.infrastructure.authentication.session.session_gateway import SessionDoesNotExistError


def setup_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(auth_exceptions.UnauthorizedError, create_exception_handler(401))
    app.add_exception_handler(auth_exceptions.IncorrectPasswordError, create_exception_handler(401))
    app.add_exception_handler(user_exceptions.UserAlreadyExistsError, create_exception_handler(409))
    app.add_exception_handler(user_exceptions.UserDoesNotExistError, create_exception_handler(404))
    app.add_exception_handler(movie_exceptions.MovieAlreadyExistsError, create_exception_handler(409))
    app.add_exception_handler(movie_exceptions.MovieDoesNotExistError, create_exception_handler(404))
    app.add_exception_handler(movie_rating_exceptions.MovieRatingAlreadyExistsError, create_exception_handler(409))
    app.add_exception_handler(movie_rating_exceptions.MovieRatingDoesNotExistError, create_exception_handler(404))
    app.add_exception_handler(SessionDoesNotExistError, create_exception_handler(401))


def create_exception_handler(status_code: int, data: dict[str, Any] | None = None) -> Callable:
    async def exception_handler(request: Request, exc: Exception) -> JSONResponse:
        return JSONResponse(content=data, status_code=status_code)
    return exception_handler