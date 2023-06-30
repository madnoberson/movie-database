from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class RateMovieOutSchema(BaseModel):

    new_movie_rating: float
    new_movie_rating_count: int
    user_rating: float
    created_at: datetime


class ReevaluateMovieOutSchema(BaseModel):

    new_user_rating: float
    new_movie_rating: float
    new_movie_rating_count: int


class MovieDoesNotExistErrorSchema(BaseModel):

    movie_id: UUID


class UserMovieRatingDoesNotExistErrorSchema(BaseModel):

    movie_id: UUID


class UserMovieRatingAleadyExistsErrorSchema(BaseModel):

    movie_id: UUID

