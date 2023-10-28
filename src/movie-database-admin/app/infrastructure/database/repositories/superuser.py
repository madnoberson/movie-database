from uuid import UUID

from asyncpg.connection import Connection

from app.domain.models.superuser import Superuser
from app.application.common.interfaces.repositories import SuperuserRepository
from app.infrastructure.database.mappers import as_domain_model


class SuperuserRepositoryImpl(SuperuserRepository):

    def __init__(self, connection: Connection) -> None:
        self.connection = connection

    async def check_superuser_exists(self, username: str) -> bool:
        data = await self.connection.fetchval(
            "SELECT 1 FROM superusers su WHERE su.username = $1 LIMIT 1", username
        )
        return bool(data)
    
    async def save_superuser(self, superuser: Superuser) -> None:
        await self.connection.execute(
            """
            INSERT INTO superusers (
                id, username, email, password, is_active,
                permissions, created_at
            )
            VALUES ($1, $2, $3, $4, $5, $6, $7)
            """,
            superuser.id, superuser.username, superuser.email,
            superuser.password, superuser.is_active,
            [permission.value for permission in superuser.permissions],
            superuser.created_at
        )
    
    async def get_superuser(self, superuser_id: UUID) -> Superuser | None:
        data = await self.connection.fetchrow(
            "SELECT * FROM superusers su WHERE su.id = $1 LIMIT 1", superuser_id
        )
        return as_domain_model(Superuser, data) if data else None
    
    async def update_user(self, superuser: Superuser) -> None:
        await self.connection.execute(
            """
            UPDATE users u SET
                username = $1, email = $2, password = $3,
                is_active = $4, permissions = $5
            WHERE u.id = $6
            """,
            superuser.username, superuser.email, superuser.password,
            superuser.is_active,
            [permission.value for permission in superuser.permissions],
            superuser.id
        )