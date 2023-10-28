from pydantic import BaseModel

from app.domain.constants import SuperUserPermissionEnum


class CreateSuperuserSchema(BaseModel):

    username: str
    email: str
    password: str
    permissions: list[SuperUserPermissionEnum]