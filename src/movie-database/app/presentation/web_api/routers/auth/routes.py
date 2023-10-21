from typing import Annotated, Literal

from fastapi import Depends, Response

from app.application.commands.registration.register import InputDTO as RegisterDTO
from app.application.queries.auth.login import InputDTO as LoginDTO
from app.infrastructure.authentication.session.session_gateway import Session, AuthSessionGateway
from app.presentation.handler_factory import HandlerFactory
from app.presentation.web_api.depends_stub import Stub
from . import requests


async def register(
    ioc: Annotated[HandlerFactory, Depends()],
    session_gateway: Annotated[AuthSessionGateway, Depends(Stub(AuthSessionGateway))],
    data: requests.RegisterSchema,
    response: Response
) -> Literal[True]:
    async with ioc.register() as register:
        result = await register(RegisterDTO(username=data.username, password=data.password))
        session_id = await session_gateway.save_session(Session(user_id=result.user_id))
        response.set_cookie(key="session_id", value=session_id, httponly=True)
    return True


async def login(
    ioc: Annotated[HandlerFactory, Depends()],
    session_gateway: Annotated[AuthSessionGateway, Depends(Stub(AuthSessionGateway))],
    data: requests.LoginSchema,
    response: Response
) -> Literal[True]:
    async with ioc.login() as login:
        result = await login(LoginDTO(username=data.username, password=data.password))
        session_id = await session_gateway.save_session(Session(user_id=result.user_id))
        response.set_cookie(key="session_id", value=session_id, httponly=True)
    return True