from datetime import datetime

from pydantic import BaseModel

from src.presentation.api.common.error_schemas import BaseErrorSchema


class RateMovieOutSchema(BaseModel):

    new_movie_rating: float
    new_movie_rating_count: int
    user_rating: float
    created_at: datetime


def get_rate_movie_responses() -> dict:
    return {
        201: {"model": RateMovieOutSchema},
        401: {"model": BaseErrorSchema},
        404: {"model": BaseErrorSchema},
        409: {"model": BaseErrorSchema}
    }


class ReevaluateMovieOutSchema(BaseModel):

    new_user_rating: float
    new_movie_rating: float
    new_movie_rating_count: int



def get_reevaluate_movie_responses() -> dict:

    return {
        200: {"model": RateMovieOutSchema},
        401: {"model": BaseErrorSchema},
        404: {"model": BaseErrorSchema}
    }


class RemoveUserMovieRatingOutSchema(BaseModel):

    new_movie_rating: float
    new_movie_rating_count: int


def get_remove_movie_rating_responses() -> dict:
    return {
        200: {"model": RemoveUserMovieRatingOutSchema},
        401: {"model": BaseErrorSchema},
        404: {"model": BaseErrorSchema}
    }
