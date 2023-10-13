from typing import Annotated, Literal

from fastapi import Depends, Response

from app.application.commands.registration import register as register_handler
from app.application.queries.authentication import login as login_handler
from app.infrastructure.authentication.session import Session, AuthSessionGateway
from app.presentation.web_api.depends_stub import Stub
from . import requests


async def register(
    register: Annotated[register_handler.Register, Depends(Stub(register_handler.Register))],
    session_gateway: Annotated[AuthSessionGateway, Depends(Stub(AuthSessionGateway))],
    data: requests.RegisterSchema,
    response: Response
) -> Literal[True]:
    dto = register_handler.InputDTO(username=data.username, password=data.password)
    result = await register(dto)
    session_id = await session_gateway.save_session(Session(user_id=result.user_id))
    response.set_cookie(key="session_id", value=session_id, httponly=True)
    return True


async def login(
    login: Annotated[login_handler.Login, Depends(Stub(login_handler.Login))],
    session_gateway: Annotated[AuthSessionGateway, Depends(Stub(AuthSessionGateway))],
    data: requests.LoginSchema,
    response: Response
) -> Literal[True]:
    dto = login_handler.InputDTO(username=data.username, password=data.password)
    result = await login(dto)
    session_id = await session_gateway.save_session(Session(user_id=result.user_id))
    response.set_cookie(key="session_id", value=session_id, httponly=True)
    return True