from dataclasses import dataclass
from uuid import UUID

from asyncpg import Connection
from asyncpg.transaction import Transaction

from src.domain.user import User
from src.domain.profile import Profile
from src.application.common.interfaces.database_gateway import DatabaseGateway
from .utils import as_domain_model


@dataclass(frozen=True, slots=True)
class AsyncpgDatabaseGateway(DatabaseGateway):

    connection: Connection
    transaction: Transaction

    async def check_user_exists(self, email: str) -> bool:
        data = await self.connection.fetchval(
            "SELECT 1 FROM users u WHERE u.email = $1 LIMIT 1", email
        )
        return bool(data)
    
    async def save_user(self, user: User) -> None:
        await self.connection.execute(
            """
            INSERT INTO users (id, email, encoded_password, created_at)
            VALUES ($1, $2, $3, $4)
            """,
            user.id, user.email, user.encoded_password, user.created_at
        )
    
    async def get_user(self, user_id: UUID) -> User | None:
        data = await self.connection.fetchrow(
            "SELECT u.* FROM users u WHERE u.id = $1", user_id
        )
        return None if data is None else as_domain_model(User, data)
    
    async def update_user(self, user: User) -> None:
        await self.connection.execute(
            """
            UPDATE users u SET (email = $1, encoded_password $2) WHERE u.id = $3
            """,
            user.email, user.encoded_password, user.id
        )

    async def save_profile(self, profile: Profile) -> None:
        await self.connection.execute(
            "INSERT INTO profiles (id, user_id, username) VALUES ($1, $2, $3)",
            profile.id, profile.user_id, profile.username
        )
    
    async def get_profile(self, profile_id: UUID) -> Profile | None:
        data = await self.connection.fetchrow(
            "SELECT p.* FROM profiles p WHERE p.id = $1", profile_id
        )
        return None if data is None else as_domain_model(Profile, data)

    async def update_profile(self, profile: Profile) -> None:
        await self.connection.execute(
            "UPDATE profiles p SET (username = $1) WHERE p.id = $2", 
            profile.username, profile.id
        )
    
    async def commit(self) -> None:
        await self.transaction.commit()