from uuid import UUID

from asyncpg.connection import Connection

from app.domain.models.enrichment_task import EnrichmentTask
from app.application.common.interfaces.repositories import EnrichmentTaskRepository
from app.infrastructure.database.mappers import as_domain_model


class EnrichmentTaskRepositoryImpl(EnrichmentTaskRepository):

    def __init__(self, connection: Connection) -> None:
        self.connection = connection

    async def check_enrichment_task_exists(self, kinopoisk_id: str) -> bool:
        data = await self.connection.fetchval(
            "SELECT 1 FROM enrichment_tasks et WHERE et.kinopoisk_id = $1 LIMIT 1",
            kinopoisk_id
        )
        return bool(data)
    
    async def save_enrichment_task(self, enrichment_task: EnrichmentTask) -> None:
        await self.connection.execute(
            """
            INSERT INTO enrichment_tasks
            (
                id, user_id, enrichment_type, kinopoisk_id,
                created_at, movie_id, finished_at
            )
            VALUES ($1, $2, $3, $4, $5, $6, $7)
            """,
            enrichment_task.id, enrichment_task.user_id, enrichment_task.enrichment_type,
            enrichment_task.kinopoisk_id, enrichment_task.created_at, enrichment_task.movie_id,
            enrichment_task.finished_at
        )
    
    async def get_enrichment_task(self, enrichment_task_id: UUID) -> EnrichmentTask | None:
        data = await self.connection.fetchrow(
            "SELECT et.* FROM enrichment_tasks et WHERE et.id = $1 LIMIT 1",
            enrichment_task_id
        )
        return as_domain_model(EnrichmentTask, dict(data)) if data else None

    async def update_enrichment_task(self, enrichment_task: EnrichmentTask) -> None:
        await self.connection.execute(
            "UPDATE enrichment_tasks et SET movie_id = $1, finished_at = $2 WHERE et.id = $3",
            enrichment_task.movie_id, enrichment_task.finished_at, enrichment_task.id
        )