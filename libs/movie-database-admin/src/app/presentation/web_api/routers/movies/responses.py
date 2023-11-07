from uuid import UUID

from pydantic import BaseModel


class CreateMovieOutSchema(BaseModel):

    movie_id: UUID
    