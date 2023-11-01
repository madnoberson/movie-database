from typing import Callable, Any

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.domain.exceptions import access as access_exceptions
from app.application.common.exceptions import auth as auth_exceptions
from app.application.common.exceptions import user as user_exceptions
from app.application.common.exceptions import superuser as superuser_exceptions
from app.infrastructure.authentication.session.session.gateway import SessionDoesNotExistError


def setup_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(access_exceptions.AccessDeniedError, create_exception_handler(403))
    app.add_exception_handler(auth_exceptions.UnauthorizedError, create_exception_handler(401))
    app.add_exception_handler(auth_exceptions.IncorrectPasswordError, create_exception_handler(401))
    app.add_exception_handler(user_exceptions.UserDoesNotExistError, create_exception_handler(404))
    app.add_exception_handler[superuser_exceptions.SuperuserAlreadyExistsError, create_exception_handler(409)]
    app.add_exception_handler[superuser_exceptions.SuperuserDoesNotExistError, create_exception_handler(404)]
    app.add_exception_handler(SessionDoesNotExistError, create_exception_handler(401))


def create_exception_handler(status_code: int, data: dict[str, Any] | None = None) -> Callable:
    async def exception_handler(request: Request, exc: Exception) -> JSONResponse:
        return JSONResponse(content=data, status_code=status_code)
    return exception_handler