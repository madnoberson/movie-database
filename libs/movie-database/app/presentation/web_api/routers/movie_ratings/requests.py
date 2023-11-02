from pydantic import BaseModel


class RateMovieSchema(BaseModel):

    rating: float