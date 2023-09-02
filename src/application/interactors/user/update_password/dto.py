from dataclasses import dataclass
from uuid import UUID

@dataclass(frozen=True, slots=True)
class UpdatePasswordDTO:

    user_id: UUID
    password: str
