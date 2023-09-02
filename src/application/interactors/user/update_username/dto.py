from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True, slots=True)
class UpdateUsernameDTO:

    user_id: UUID
    username: str
