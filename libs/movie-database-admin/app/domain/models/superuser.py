from dataclasses import dataclass
from datetime import datetime
from enum import IntEnum
from uuid import UUID

from .model import Model


class SuperUserPermissionEnum(IntEnum):

    SUPERUSERS = 0
    USERS = 1



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
    
    def change_password(self, password: str) -> None:
        self.password = password