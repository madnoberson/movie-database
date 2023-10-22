from typing import Callable, Any

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.application.common.exceptions import auth as auth_exceptions
from app.application.common.exceptions import user as user_exceptions
from app.application.common.exceptions import adding_task as adding_task_exceptions
from app.infrastructure.authentication.session.session_gateway import SessionDoesNotExistError


def setup_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(auth_exceptions.UnauthorizedError, create_exception_handler(401))
    app.add_exception_handler(auth_exceptions.PasswordIsNotCorrectError, create_exception_handler(401))
    app.add_exception_handler(user_exceptions.UserAlreadyExistsError, create_exception_handler(409))
    app.add_exception_handler(user_exceptions.UserDoesNotExistError, create_exception_handler(404))
    app.add_exception_handler(adding_task_exceptions.AddingTaskAlreadyExistsError, create_exception_handler(409))
    app.add_exception_handler(adding_task_exceptions.AddingTaskDoesNotExistError, create_exception_handler(404))
    app.add_exception_handler(SessionDoesNotExistError, create_exception_handler(401))


def create_exception_handler(status_code: int, data: dict[str, Any] | None = None) -> Callable:
    async def exception_handler(request: Request, exc: Exception) -> JSONResponse:
        return JSONResponse(content=data, status_code=status_code)
    return exception_handler