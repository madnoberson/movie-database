from typing import Annotated
from fastapi import Depends, Response

from src.presentation.api.interactor import ApiInteractor
from src.presentation.api.authenticator import ApiAuthenticator
from src.application.commands.register.command import RegisterCommand
from src.application.queries.login.query import LoginQuery
from .requests import RegisterSchema, LoginSchema


def register(
    interactor: Annotated[ApiInteractor, Depends()],
    authenticator: Annotated[ApiAuthenticator, Depends()],
    response: Response,
    data: RegisterSchema
) -> bool:
    command = RegisterCommand(
        username=data.username,
        password=data.password
    )
    result = interactor.handle_register_command(command)

    access_token = authenticator.create_access_token(
        user_id=result.user_id
    )
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True
    )
    return True


def login(
    interactor: Annotated[ApiInteractor, Depends()],
    authenticator: Annotated[ApiAuthenticator, Depends()],
    response: Response,
    data: LoginSchema
) -> bool:
    query = LoginQuery(
        username=data.username,
        password=data.password
    )
    result = interactor.handle_login_query(query)

    access_token = authenticator.create_access_token(
        user_id=result.user_id
    )
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True
    )
    return True
