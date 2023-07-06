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


def get_rate_movie_responses() -> dict:
    return {
        201: {"model": RateMovieOutSchema},
        401: {"model": ""},
        404: {"model": MovieDoesNotExistErrorSchema},
        409: {"model": UserMovieRatingAleadyExistsErrorSchema}
    }


def get_reevaluate_movie_responses() -> dict:
    return {
        201: {"model": RateMovieOutSchema},
        404: {"model": MovieDoesNotExistErrorSchema},
        409: {"model": UserMovieRatingDoesNotExistErrorSchema}
    }


def get_remove_movie_rating_responses() -> dict:
    return {}
