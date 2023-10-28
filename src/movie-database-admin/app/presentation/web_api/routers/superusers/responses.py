from uuid import UUID

from pydantic import BaseModel


class CreateSuperuserOutSchema(BaseModel):

    superuser_id: UUID