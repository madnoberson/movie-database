from dataclasses import dataclass
from uuid import UUID

from asyncpg import Connection
from asyncpg.transaction import Transaction

from src.domain.user import User
from src.domain.profile import Profile
from src.application.common.interfaces.dbw_gateway import DatabaseWritingGateway
from src.infrastructure.application.utils import as_domain_model


@dataclass(frozen=True, slots=True)
class AsyncpgDatabaseWritingGateway(DatabaseWritingGateway):

    connection: Connection
    transaction: Transaction

    async def check_user_exists(
        self, username: str | None = None, user_id: UUID | None = None
    ) -> bool:
        if username is not None:
            user_exists = await self.connection.fetchval(
                "SELECT 1 FROM users u WHERE u.username LIMIT 1", username
            )
            return bool(user_exists)
        user_exists = await self.connection.fetchval(
            "SELECT 1 FROM users u WHERE u.id = $1", user_id
        )
        return bool(user_exists)

    async def save_user(self, user: User) -> None:
        await self.connection.execute(
            """
            INSERT INTO users (id, username, email, encoded_password, created_at)
            VALUES ($1, $2, $3, $4, $5)
            """,
            user.id, user.username, user.email, user.encoded_password, user.created_at
        )
    
    async def get_user(self, user_id: UUID) -> User | None:
        data = await self.connection.fetchrow(
            "SELECT u.* FROM users u WHERE u.id = $1 LIMIT 1", user_id
        )
        return as_domain_model(User, data) if data else None

    async def update_user(self, user: User) -> None:
        await self.connection.execute(
            """
            UPDATE users u
            SET username = $1, email = $2, encoded_password = $3 WHERE u.id = $4
            """,
            user.id
        )
    
    async def save_profile(self, profile: Profile) -> None:
        await self.connection.execute(
            """
            INSERT INTO users
            (
                id, user_id, rated_movies, rated_series,
                reviews, followers, following, favourites
            )
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
            """,
            profile.id, profile.user_id, profile.rated_movies, profile.rated_series,
            profile.reviews, profile.followers, profile.following, profile.favourites
        )
    
    async def get_profile(self, profile_id: UUID) -> Profile | None:
        data = await self.connection.fetchrow(
            "SELECT p.* FROM profiles p WHERE p.id = $1 LIMIT 1", profile_id
        )
        return as_domain_model(Profile, data) if data else None

    async def update_profile(self, profile: Profile) -> None:
        await self.connection.execute(
            """
            UPDATE profiles p
            SET
                rated_movies = $1, rated_series = $2, reviews = $3,
                followers = $4, following = $5, favourites = $6
            WHERE p.id = $7
            """,
            profile.rated_movies, profile.rated_series, profile.reviews,
            profile.followers, profile.following, profile.favourites, profile.id
        )
    
    async def commit(self) -> None:
        await self.transaction.commit()