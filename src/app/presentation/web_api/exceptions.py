from typing import Callable, Any

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.application.common.exceptions import authentication as auth_exceptions
from app.application.common.exceptions import user as user_exceptions


def setup_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(auth_exceptions.UnauthorizedError, create_exception_handler(401))
    app.add_exception_handler(auth_exceptions.PasswordIsNotCorrectError, create_exception_handler(401))
    app.add_exception_handler(user_exceptions.UserAlreadyExistsError, create_exception_handler(409))
    app.add_exception_handler(user_exceptions.UserDoesNotExistError, create_exception_handler(404))


def create_exception_handler(status_code: int, data: dict[str, Any] = {}) -> Callable:
    async def exception_handler(request: Request, exc: Exception) -> JSONResponse:
        return JSONResponse(content=data, status_code=status_code)
    return exception_handler