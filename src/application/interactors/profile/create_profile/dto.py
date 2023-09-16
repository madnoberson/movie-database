from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True, slots=True)
class CreateProfileDTO:

    user_id: UUID
    username: str


@dataclass(frozen=True, slots=True)
class CreateProfileResultDTO:

    profile_id: UUID
