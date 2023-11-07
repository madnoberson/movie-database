from pydantic import BaseModel, Field


class RateMovieSchema(BaseModel):

    rating: float = Field(ge=0.5, le=10)