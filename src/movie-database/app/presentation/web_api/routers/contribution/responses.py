from uuid import UUID

from pydantic import BaseModel


class CreateAddingTaskOutSchema(BaseModel):

    adding_task_id: UUID