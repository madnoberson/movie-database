from uuid import UUID

from pydantic import BaseModel

from app.domain.models.superuser import SuperUserPermissionEnum


class CreateSuperuserSchema(BaseModel):

    username: str
    email: str
    password: str
    permissions: list[SuperUserPermissionEnum]


class ChangeSuperuserPasswordSchema(BaseModel):

    superuser_id: UUID
    new_password: str