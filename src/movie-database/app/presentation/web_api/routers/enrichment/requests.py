from pydantic import BaseModel


class CreateEnrichmentTaskSchema(BaseModel):

    kinopisk_id: str