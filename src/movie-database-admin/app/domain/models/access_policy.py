from dataclasses import dataclass
from uuid import UUID

from app.domain.constants import SuperUserPermissionEnum
from .model import Model


@dataclass(slots=True)
class AccessPolicy(Model):

    superuser_id: UUID
    is_active: bool
    permissions: list[SuperUserPermissionEnum]

    @classmethod
    def create(
        cls, superuser_id: UUID, is_active: bool,
        permissions: list[SuperUserPermissionEnum]
    ) -> "AccessPolicy":
        return AccessPolicy(
            id=superuser_id, is_active=is_active,
            permissions=permissions
        )