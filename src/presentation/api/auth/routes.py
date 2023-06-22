from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from src.presentation.interactor_factory import InteractorFactory
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
from .responses import AuthResponseSchema
from .errors import UsernameAlreadyExistsErrorSchema


auth_router = APIRouter(prefix="/auth", tags=["auth"])

regitser_route_responses = {
    409: {"model": UsernameAlreadyExistsErrorSchema}
}


@auth_router.post(
    path="/register/",
    response_model=AuthResponseSchema,
    status_code=201,
    responses=regitser_route_responses
)
def register(
    ioc: Annotated[InteractorFactory, Depends()],
    auth: Annotated[ApiAuthenticator, Depends()],
    data: RegisterSchema
):
    with ioc.register_command_handler() as handle:

        command = RegisterCommand(
            username=data.username,
            password=data.password
        )
        result = handle(command)

        match result:

            case Result(RegisterCommandResult(), None):
                access_token = auth.create_access_token(
                    user_id=result.value.user_id
                )
                refresh_token = auth.create_refresh_token(
                    user_id=result.value.user_id
                )
                return AuthResponseSchema(
                    access_token=access_token,
                    refresh_token=refresh_token
                )
            
            case Result(None, UsernameAlreadyExistsError()):
                return JSONResponse(
                    status_code=409,
                    content={"username": result.error.username}
                )


login_route_responses = {
    404: {"model": UsernameDoesNotExistError}
}


@auth_router.post(
    path="/login/",
    response_model=AuthResponseSchema,
    responses=login_route_responses
)
def login(
    ioc: Annotated[InteractorFactory, Depends()],
    auth: Annotated[ApiAuthenticator, Depends()],
    data: LoginSchema
):
    with ioc.login_query_handler() as handle:

        query = LoginQuery(
            username=data.username,
            password=data.password
        )
        result = handle(query)

        match result:

            case Result(LoginQueryResult(), None):
                access_token = auth.create_access_token(
                    user_id=result.value.user_id
                )
                refresh_token = auth.create_refresh_token(
                    user_id=result.value.user_id
                )
                return AuthResponseSchema(
                    access_token=access_token,
                    refresh_token=refresh_token
                )

            case Result(None, UsernameDoesNotExistError()):
                return JSONResponse(
                    status_code=404,
                    content={"username": result.error.username}
                )
            
            case Result(None, PasswordIsIncorrectError()):
                return None