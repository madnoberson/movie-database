from uuid import UUID

from pydantic import BaseModel


class CreateEnrichmentTaskOutSchema(BaseModel):

    enrichment_task_id: UUID