from uuid import UUID

from pydantic import BaseModel


class UsernameChanged(BaseModel):

    user_id: UUID
    new_username: str