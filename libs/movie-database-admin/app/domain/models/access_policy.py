from dataclasses import dataclass
from uuid import UUID

from .model import Model
from .superuser import SuperUserPermissionEnum


@dataclass(slots=True)
class AccessPolicy(Model):

    superuser_id: UUID | None
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
    
    @property
    def is_unauthorized(self) -> bool:
        return self.superuser_id is None