from typing import Annotated
from uuid import UUID

from fastapi import Depends, HTTPException

from src.presentation.api.interactor import ApiInteractor
from src.presentation.api.authenticator import get_user_id
from src.application.commands.rate_movie.command import RateMovieCommand
from src.application.commands.reevaluate_movie.command import ReevaluateMovieCommand
from src.application.commands.remove_user_movie_rating.command import RemoveUserMovieRatingCommand
from .requests import RateMovieSchema, ReevaluateMovieSchema
from .responses import RateMovieOutSchema, ReevaluateMovieOutSchema


def rate_movie(
    interactor: Annotated[ApiInteractor, Depends()],
    user_id: Annotated[UUID | None, Depends(get_user_id)],
    data: RateMovieSchema
) -> RateMovieOutSchema:
    if user_id is None:
        raise HTTPException(401)

    command = RateMovieCommand(
        user_id=user_id,
        movie_id=data.movie_id,
        rating=data.rating
    )
    result = interactor.handle_rate_movie_command(command)

    return RateMovieOutSchema(
        new_movie_rating=result.new_movie_rating,
        new_movie_rating_count=result.new_movie_rating_count,
        user_rating=result.user_rating,
        created_at=result.user_rating_created_at
    )

def reevaluate_movie(
    interactor: Annotated[ApiInteractor, Depends()],
    user_id: Annotated[UUID | None, Depends(get_user_id)],
    movie_id: UUID,
    data: ReevaluateMovieSchema
) -> None:
    if not user_id:
        raise HTTPException(401)
    
    command = ReevaluateMovieCommand(
        user_id=user_id,
        movie_id=movie_id,
        new_rating=data.new_rating
    )
    result = interactor.handle_reevaluate_movie_command(command)

    return ReevaluateMovieOutSchema(
        new_movie_rating=result.new_movie_rating,
        new_user_rating=result.new_user_rating
    )
        

def remove_movie_rating(
    interactor: Annotated[ApiInteractor, Depends()],
    user_id: Annotated[UUID | None, Depends(get_user_id)],
    movie_id: UUID
):
    if not user_id:
        raise HTTPException(401)
    