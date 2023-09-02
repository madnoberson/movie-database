from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True, slots=True)
class UpdateEmailDTO:

    user_id: UUID
    email: str