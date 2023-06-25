from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True, slots=True)
class UserDoesNotExistError(Exception):
    
    user_id: UUID
