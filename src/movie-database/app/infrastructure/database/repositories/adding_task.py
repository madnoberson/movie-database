from uuid import UUID

from asyncpg.connection import Connection

from app.domain.models.adding_task import AddingTask
from app.application.common.interfaces.repositories import AddingTaskRepository
from app.infrastructure.database.mappers import as_domain_model


class AddingTaskRepositoryImpl(AddingTaskRepository):

    def __init__(self, connection: Connection) -> None:
        self.connection = connection

    async def check_adding_task_exists(self, kinopoisk_id: str) -> bool:
        data = await self.connection.fetchval(
            "SELECT 1 FROM adding_tasks at WHERE at.kinopoisk_id = $1 LIMIT 1",
            kinopoisk_id
        )
        return bool(data)
    
    async def save_adding_task(self, adding_task: AddingTask) -> None:
        await self.connection.execute(
            """
            INSERT INTO adding_tasks
            (
                id, creator_id, adding_type, kinopoisk_id,
                created_at, related_to, finished_at
            )
            VALUES ($1, $2, $3, $4, $5, $6, $7)
            """,
            adding_task.id, adding_task.creator_id, adding_task.adding_type,
            adding_task.kinopoisk_id, adding_task.created_at, adding_task.related_to,
            adding_task.finished_at
        )
    
    async def get_adding_task(self, adding_task_id: UUID) -> AddingTask | None:
        data = await self.connection.fetchrow(
            "SELECT at.* FROM adding_tasks at WHERE at.id = $1 LIMIT 1",
            adding_task_id
        )
        return as_domain_model(AddingTask, dict(data)) if data else None

    async def update_adding_task(self, adding_task: AddingTask) -> None:
        await self.connection.execute(
            "UPDATE adding_tasks at SET related_to = $1, finished_at = $2 WHERE at.id = $3",
            adding_task.related_to, adding_task.finished_at, adding_task.id
        )