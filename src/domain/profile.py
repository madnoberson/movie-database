from dataclasses import dataclass
from uuid import UUID


@dataclass(slots=True)
class Profile:

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