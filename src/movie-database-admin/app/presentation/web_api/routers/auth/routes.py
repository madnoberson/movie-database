from typing import Annotated, Literal

from fastapi import Depends, Response

from app.application.queries.auth.login import InputDTO as LoginDTO, OutputDTO as LogintResultDTO
from app.infrastructure.authentication.session.access_policy.gateway import AccessPolicy, AccessPolicyGateway
from app.infrastructure.authentication.session.session.gateway import Session, SessionGateway
from app.presentation.handler_factory import HandlerFactory
from app.presentation.web_api.depends_stub import Stub
from . import requests


async def login(
    access_policy_gateway: Annotated[AccessPolicyGateway, Depends(Stub(AccessPolicyGateway))],
    session_gateway: Annotated[SessionGateway, Depends(Stub(SessionGateway))],
    ioc: Annotated[HandlerFactory, Depends()],
    data: requests.LoginSchema,
    response: Response
) -> Literal[True]:
    async with ioc.login() as login:
        dto = LoginDTO(username=data.username, password=data.password)
        result: LogintResultDTO = await login(dto)

        session = Session(superuser_id=result.superuser_id)
        session_id = await session_gateway.save_session(session)

        access_policy = AccessPolicy(
            superuser_id=result.superuser_id, is_active=result.is_active,
            permissions=result.permissions
        )
        await access_policy_gateway.save_access_policy(access_policy)
        
        response.set_cookie(key="session_id", value=session_id, httponly=True)
    return True