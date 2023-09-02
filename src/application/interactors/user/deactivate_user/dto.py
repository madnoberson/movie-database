from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True, slots=True)
class DeactivateUserDTO:

    user_id: UUID
