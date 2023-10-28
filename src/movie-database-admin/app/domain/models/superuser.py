from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from app.domain.constants import SuperUserPermissionEnum
from .model import Model


@dataclass(slots=True)
class Superuser(Model):

    id: UUID
    username: str
    email: str
    password: str
    is_active: bool
    permissions: list[SuperUserPermissionEnum]
    created_at: datetime

    @classmethod
    def create(
        cls, superuser_id: UUID, username: str, email: str,
        password: str, permissions: list[SuperUserPermissionEnum],
        created_at: datetime
    ) -> "Superuser":
        return Superuser(
            id=superuser_id, username=username, email=email,
            password=password, is_active=False, permissions=permissions,
            created_at=created_at
        )