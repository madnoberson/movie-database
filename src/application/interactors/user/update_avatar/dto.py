from dataclasses import dataclass
from io import BytesIO
from uuid import UUID


@dataclass(frozen=True, slots=True)
class UpdateAvatarDTO:

    user_id: UUID
    avatar: BytesIO