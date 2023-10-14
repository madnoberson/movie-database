from typing import Annotated

from fastapi import Depends, Cookie

from app.infrastructure.authentication.session import (
    AuthSessionGateway, SoftSessionIdentityProvider, StrictSessionIdentityProvider
)
from app.presentation.web_api.depends_stub import Stub


def get_soft_identity_provider(
    session_gateway: Annotated[AuthSessionGateway, Depends(Stub(AuthSessionGateway))],
    session_id: Annotated[str, Cookie()]
) -> SoftSessionIdentityProvider:
    """
    Returns `SoftIdentityProvider` that does nothing if user is not authorized
    """
    return SoftSessionIdentityProvider(session_id, session_gateway)


def get_strict_identity_provider(
    session_gateway: Annotated[AuthSessionGateway, Depends(Stub(AuthSessionGateway))],
    session_id: Annotated[str, Cookie()]
) -> StrictSessionIdentityProvider:
    """
    Returns `StrictIdentityProvider` that raises `UnauthorizedError`
    if user is not authorized
    """
    return StrictSessionIdentityProvider(session_id, session_gateway)