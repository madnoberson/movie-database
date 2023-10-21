from pydantic import BaseModel

from app.domain.models.enrichment_task import EnrichmentTaskTypeEnum


class CreateEnrichmentTaskSchema(BaseModel):

    kinopisk_id: str
    enrichment_type: EnrichmentTaskTypeEnum