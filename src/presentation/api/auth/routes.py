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
from .requests import RegisterSchema
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
    with ioc.register() as register:

        command = RegisterCommand(
            username=data.username,
            password=data.password
        )
        result = register(command)

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


@auth_router.post(path="/login/")
def login(
    ioc: Annotated[InteractorFactory, Depends()],
    auth: Annotated[ApiAuthenticator, Depends()],
):
    ...