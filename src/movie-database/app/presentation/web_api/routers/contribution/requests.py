from pydantic import BaseModel

from app.domain.models.adding_task import AddingTaskTypeEnum


class CreateAddingTaskSchema(BaseModel):

    kinopisk_id: str
    adding_type: AddingTaskTypeEnum