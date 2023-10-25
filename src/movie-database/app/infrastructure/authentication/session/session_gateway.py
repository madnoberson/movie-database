from dataclasses import dataclass
from datetime import timedelta
from uuid import UUID, uuid4

from redis.asyncio import Redis


class SessionDoesNotExistError(Exception):
    ...


@dataclass(frozen=True, slots=True)
class Session:

    user_id: UUID


class SessionGateway:

    def __init__(
        self,
        connection: Redis,
        session_lifetime: timedelta
    ) -> None:
        self.connection = connection
        self.session_lifetime = session_lifetime

    async def save_session(self, session: Session) -> str:
        """
        Deletes old sesssion, saves new one and returns its id
        """
        await self._delete_session(user_id=session.user_id)
        return await self._save_session(session)

    async def get_session(self, session_id: UUID) -> Session:
        """
        Returns session if exists, otherwise raises `SessionDoesNotExistError`
        """
        data = await self.connection.hgetall(f"auth_sessions:session_id:{session_id}")
        if not data:
            raise SessionDoesNotExistError()
        return Session(user_id=UUID(data["user_id"]))
    
    async def _save_session(self, session: Session) -> str:
        session_id = self._create_session_id()
        session_key = f"auth_sessions:session_id:{session_id}"
        session_data = {"user_id": session.user_id.hex}

        await self.connection.set(
            name=f"auth_sessions:user_id:{session.user_id.hex}",
            value=session_id, ex=self.session_lifetime
        )
        await self.connection.hset(name=session_key, mapping=session_data)
        await self.connection.expire(name=session_key, time=self.session_lifetime)

        return session_id
    
    async def _delete_session(self, user_id: UUID) -> None:
        session_id = await self.connection.get(f"auth_sessions:user_id:{user_id.hex}")
        if session_id is not None:
            await self.connection.delete(f"auth_sessions:session_id:{session_id}")

    def _create_session_id(self) -> str:
        return uuid4().hex