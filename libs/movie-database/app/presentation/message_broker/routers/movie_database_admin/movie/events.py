from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class MovieCreated(BaseModel):

    movie_id: UUID
    en_name: str
    created_at: datetime