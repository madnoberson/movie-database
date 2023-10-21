from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.models.enrichment_task import EnrichmentTask


class EnrichmentTaskRepository(ABC):

    @abstractmethod
    async def save_enrichment_task(self, enrichment_task: EnrichmentTask) -> None:
        raise NotImplementedError
    
    @abstractmethod
    async def get_enrichment_task(self, enrichment_task_id: UUID) -> EnrichmentTask | None:
        raise NotImplementedError
    
    @abstractmethod
    async def update_enrichment_task(self, enrichment_task: EnrichmentTask) -> None:
        raise NotImplementedError