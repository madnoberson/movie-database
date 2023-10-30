from asyncpg.connection import Connection

from app.domain.models.user import User
from app.application.common.interfaces.repositories import UserRepository


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
            INSERT INTO users (id, username, created_at)
            VALUES ($1, $2, $3)
            """,
            user.id, user.username, user.created_at
        )