from uuid import UUID

from asyncpg.connection import Connection

from app.domain.models.user import User
from app.application.common.interfaces.repositories import UserRepository
from app.infrastructure.database.mappers import as_domain_model


class UserRepositoryImpl(UserRepository):

    def __init__(self, connection: Connection) -> None:
        self.connection = connection

    async def check_user_exists(self, username: str) -> bool:
        data = await self.connection.fetchval(
            "SELECT 1 FROM users u WHERE u.username = $1 LIMIT 1", username
        )
        return bool(data)
    
    async def save_user(self, user: User) -> None:
        await self.connection.execute(
            """
            INSERT INTO users (id, username, password, created_at)
            VALUES ($1, $2, $3, $4)
            """,
            user.id, user.username, user.password, user.created_at
        )
    
    async def get_user(self, user_id: UUID) -> User | None:
        data = await self.connection.fetchrow(
            """
            SELECT u.*, COUNT(mr.*) rated_movies_count
            FROM users u LEFT JOIN movie_ratings mr ON mr.user_id = u.id
            WHERE u.id = $1 GROUP BY u.id LIMIT 1
            """,
            user_id
        )
        print(data)
        return as_domain_model(User, data) if data else None
    
    async def update_user(self, user: User) -> None:
        await self.connection.execute(
            "UPDATE users u SET username = $1, password = $2 WHERE u.id = $3",
            user.username, user.password, user.id
        )