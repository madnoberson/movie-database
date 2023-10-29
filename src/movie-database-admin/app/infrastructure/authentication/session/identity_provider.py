from uuid import UUID

from app.domain.models.access_policy import AccessPolicy
from app.application.common.exceptions.auth import UnauthorizedError
from app.application.common.interfaces.identity_provider import IdentityProvider
from .session_gateway import SessionGateway
from .access_policy_gateway import AccessPolicyGateway


class SessionIdentityProvider(IdentityProvider):
    
    def __init__(
        self,
        session_id: UUID | None,
        session_gateway: SessionGateway,
        access_policy_gateway: AccessPolicyGateway
    ) -> None:
        self.session_id = session_id
        self.session_gateway = session_gateway
        self.access_policy_gateway = access_policy_gateway

    async def get_access_policy(self) -> AccessPolicy:
        """
        Returns current superuser access policy. \n
        Raises:
            * `UnauthorizedError` of `session_id` is `None`
            * `SessionDoesNotExistError` if session doesn't exist
            * `AccessPolicyDoesNotExistError` if access policy doesn't exist
        """
        superuser_id = await self._get_current_superuser_id()
        access_policy = await self.access_policy_gateway.get_access_policy(
            superuser_id=superuser_id
        )

        return access_policy
    
    async def _get_current_superuser_id(self) -> UUID | None:
        if not self.session_id:
            return self._handle_unauthorized()
        return await self.session_gateway.get_session(self.session_id)

    def _handle_unauthorized(self) -> None:
        raise UnauthorizedError()
