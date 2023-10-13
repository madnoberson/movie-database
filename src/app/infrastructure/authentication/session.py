from dataclasses import dataclass
from datetime import timedelta
from uuid import UUID, uuid4

from redis.asyncio import Redis

from app.application.common.exceptions.authentication import UnauthorizedError
from app.application.common.interfaces.identity_provider import IdentityProvider


class SessionDoesNotExistError(Exception):
    ...


@dataclass(frozen=True, slots=True)
class Session:

    user_id: UUID


class AuthSessionGateway:

    def __init__(
        self,
        redis: Redis,
        expire: timedelta | None = timedelta(hours=24)
    ) -> None:
        self.redis = redis
        self.expire = expire

    async def save_session(self, session: Session) -> UUID:
        """Saves session and returns its id"""
        session_id = self._create_session_id()
        session_key = f"auth_sessions:{session_id}"
        session_data = {"user_id": session.user_id.hex}
        await self.redis.hset(name=session_key, mapping=session_data)
        await self.redis.expire(name=session_key, time=self.expire)
        return session_id

    async def get_session(self, session_id: UUID) -> Session:
        """
        Returns session if exists, otherwise raises `SessionDoesNotExistError`
        """
        data = await self.redis.hgetall(f"auth_sessions:{session_id}")
        if data is None:
            raise SessionDoesNotExistError()
        return Session(user_id=UUID(data["user_id"]))
    
    def _create_session_id(self) -> str:
        return uuid4().hex


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