from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class UserCreated(BaseModel):

    user_id: UUID
    username: str
    created_at: datetime


class UsernameChanged(BaseModel):

    user_id: UUID
    new_username: str