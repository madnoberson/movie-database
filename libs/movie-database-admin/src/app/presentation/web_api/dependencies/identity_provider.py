from typing import Annotated

from fastapi import Depends, Cookie

from app.infrastructure.auth.session.session.gateway import SessionGateway
from app.infrastructure.auth.session.access_policy.gateway import AccessPolicyGateway
from app.infrastructure.auth.session.identity_provider import SessionIdentityProvider
from app.presentation.web_api.depends_stub import Stub


def get_identity_provider(
    access_policy_gateway: Annotated[AccessPolicyGateway, Depends(Stub(AccessPolicyGateway))],
    session_gateway: Annotated[SessionGateway, Depends(Stub(SessionGateway))],
    session_id: Annotated[str, Cookie()]
) -> SessionIdentityProvider:
    """
    Returns `SessionIdentityProvider` that raises `UnauthorizedError`
    if user is not authorized
    """
    return SessionIdentityProvider(session_id, session_gateway, access_policy_gateway)