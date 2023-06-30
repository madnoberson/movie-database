from typing import Annotated
from fastapi import APIRouter, Depends, Response
from fastapi.responses import JSONResponse

from src.presentation.api.interactor import ApiInteractor
from src.presentation.api.authenticator import ApiAuthenticator
from src.application.common.result import Result
from src.application.commands.register.command import (
    RegisterCommand,
    RegisterCommandResult
)
from src.application.commands.register.errors import (
    UsernameAlreadyExistsError
)
from src.application.queries.login.query import (
    LoginQuery,
    LoginQueryResult
)
from src.application.queries.login.errors import (
    UsernameDoesNotExistError,
    PasswordIsIncorrectError
)
from .requests import RegisterSchema, LoginSchema
from .responses import (
    UsernameAlreadyExistsErrorSchema,
    UsernameDoesNotExistErrorSchema,
    IncorrectPasswordErrorSchema
)


auth_router = APIRouter(prefix="/auth", tags=["auth"])


@auth_router.post(
    path="/register/",
    status_code=201,
    responses={409: {"model": UsernameAlreadyExistsErrorSchema}}
)
def register(
    interactor: Annotated[ApiInteractor, Depends()],
    authenticator: Annotated[ApiAuthenticator, Depends()],
    response: Response,
    data: RegisterSchema
):
    command = RegisterCommand(
        username=data.username,
        password=data.password
    )
    result = interactor.handle_register_command(command)

    match result:

        case Result(RegisterCommandResult() as value, None):
            access_token = authenticator.create_access_token(
                user_id=value.user_id
            )
            response.set_cookie(
                key="access_token",
                value=access_token,
                httponly=True
            )
            return True
                
        case Result(None, UsernameAlreadyExistsError() as error):
            return JSONResponse(
                status_code=409,
                content={"username": error.username}
            )
            

@auth_router.post(
    path="/login/",
    responses={
        404: {"model": UsernameDoesNotExistErrorSchema},
        401: {"model": IncorrectPasswordErrorSchema}
    }
)
def login(
    interactor: Annotated[ApiInteractor, Depends()],
    authenticator: Annotated[ApiAuthenticator, Depends()],
    response: Response,
    data: LoginSchema
):
    query = LoginQuery(
        username=data.username,
        password=data.password
    )
    result = interactor.handle_login_query(query)

    match result:

        case Result(LoginQueryResult() as value, None):
            access_token = authenticator.create_access_token(
                user_id=value.user_id
            )
            response.set_cookie(
                key="access_token",
                value=access_token,
                httponly=True
            )
            return True

        case Result(None, UsernameDoesNotExistError() as error):
            return JSONResponse(
                status_code=404,
                content={"username": error.username}
            )
        
        case Result(None, PasswordIsIncorrectError()):
            return JSONResponse(
                status_code=401,
                content={"message": "Password is incorrect"}
            )