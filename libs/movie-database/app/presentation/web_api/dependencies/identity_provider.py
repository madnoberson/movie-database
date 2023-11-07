from typing import Annotated

from fastapi import Depends, Cookie

from app.infrastructure.authentication.session.session_gateway import SessionGateway
from app.infrastructure.authentication.session import identity_providers
from app.presentation.web_api.depends_stub import Stub


def get_soft_identity_provider(
    session_gateway: Annotated[SessionGateway, Depends(Stub(SessionGateway))],
    session_id: Annotated[str, Cookie()]
) -> identity_providers.SoftSessionIdentityProvider:
    """
    Returns `SoftSessionIdentityProvider` that does nothing
    if user is not authorized
    """
    return identity_providers.SoftSessionIdentityProvider(session_id, session_gateway)


def get_strict_identity_provider(
    session_gateway: Annotated[SessionGateway, Depends(Stub(SessionGateway))],
    session_id: Annotated[str, Cookie()]
) -> identity_providers.StrictSessionIdentityProvider:
    """
    Returns `StrictSessionIdentityProvider` that raises `UnauthorizedError`
    if user is not authorized
    """
    return identity_providers.StrictSessionIdentityProvider(session_id, session_gateway)