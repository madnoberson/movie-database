from uuid import UUID

from app.application.common.exceptions.auth import UnauthorizedError
from app.application.common.interfaces.identity_provider import IdentityProvider
from .session_gateway import AuthSessionGateway


class SessionIdentityProvider(IdentityProvider):

    def __init__(
        self,
        session_id: UUID | None,
        auth_session_gateway: AuthSessionGateway
    ) -> None:
        self.session_id = session_id
        self.auth_session_gateway = auth_session_gateway

    async def get_current_user_id(self) -> UUID | None:
        if self.session_id is None:
            return await self._handle_unauthorized()
        session = await self.auth_session_gateway.get_session(self.session_id)
        return session.user_id
    
    async def _handle_unauthorized(self) -> None:
        raise NotImplementedError


class StrictSessionIdentityProvider(SessionIdentityProvider):

    async def _handle_unauthorized(self) -> None:
        raise UnauthorizedError()
    
    
class SoftSessionIdentityProvider(SessionIdentityProvider):

    async def _handle_unauthorized(self) -> None:
        return None