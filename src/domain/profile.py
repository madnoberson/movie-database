from dataclasses import dataclass
from uuid import UUID

from .base import DomainModel


@dataclass(slots=True)
class Profile(DomainModel):

    id: UUID
    user_id: UUID
    username: str

    @classmethod
    def create(
        cls, profile_id: UUID, user_id: UUID, username: str
    ) -> "Profile":
        return Profile(
            id=profile_id, user_id=user_id, username=username
        )