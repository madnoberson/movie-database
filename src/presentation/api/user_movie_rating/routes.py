from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse

from src.presentation.api.interactor import ApiInteractor
from src.presentation.api.authenticator import get_user_id
from src.application.common.result import Result
from src.application.common.errors.movie import (
    MovieDoesNotExistError
)
from src.application.common.errors.user import (
    UserDoesNotExistError
)
from src.application.common.errors.user_movie_rating import (
    UserMovieRatingDoesNotExistError
)
from src.application.commands.rate_movie.command import (
    RateMovieCommand,
    RateMovieCommandResult
)
from src.application.commands.rate_movie.errors import (
    UserMovieRatingAlreadyExistsError
)
from src.application.commands.reevaluate_movie.command import (
    ReevaluateMovieCommand,
    ReevaluateMovieCommandResult
)
from src.application.commands.remove_user_movie_rating.command import (
    RemoveUserMovieRatingCommand
)
from .requests import RateMovieSchema, ReevaluateMovieSchema
from .responses import (
    RateMovieOutSchema,
    ReevaluateMovieOutSchema,
    MovieDoesNotExistErrorSchema,
    UserMovieRatingAleadyExistsErrorSchema,
    UserMovieRatingDoesNotExistErrorSchema
)


user_movie_rating_router = APIRouter(
    prefix="/user/ratings",
    tags=["user_movie_rating"]
)


@user_movie_rating_router.post(
    path="/",
    status_code=201,
    responses={
        201: {"model": RateMovieOutSchema},
        404: {"model": MovieDoesNotExistErrorSchema},
        409: {"model": UserMovieRatingAleadyExistsErrorSchema}
    }
)
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

    match result:

        case Result(RateMovieCommandResult() as value, None):
            return RateMovieOutSchema(
                new_movie_rating=value.new_movie_rating,
                new_movie_rating_count=value.new_movie_rating_count,
                user_rating=value.user_rating,
                created_at=value.user_rating_created_at
            )

        case Result(None, UserDoesNotExistError()):
            raise HTTPException(401)

        case Result(None, MovieDoesNotExistError() as error):
            return JSONResponse(
                status_code=404,
                content={"movie_id": error.movie_id.hex}
            )

        case Result(None, UserMovieRatingAlreadyExistsError() as error):
            return JSONResponse(
                status_code=409,
                content={"movie_id": error.movie_id.hex}
            )


@user_movie_rating_router.patch(
    path="/{movie_id}/",
    responses={}
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

    match result:

        case Result(ReevaluateMovieCommandResult() as value, None):
            return ReevaluateMovieOutSchema(
                new_movie_rating=value.new_movie_rating,
                new_movie_rating_count=value.new_movie_rating_count,
                new_user_rating=value.new_user_rating
            )
        
        case Result(None, UserDoesNotExistError()):
            raise HTTPException(401)

        case Result(None, UserMovieRatingDoesNotExistError() as error):
            return JSONResponse(
                status_code=404,
                content={"movie_id": error.movie_id.hex}
            )
        

@user_movie_rating_router.delete(
    path="/{movid_id}/",
    responses={404: {"model": MovieDoesNotExistErrorSchema}}
)
def remove_movie_rating(
    interactor: Annotated[ApiInteractor, Depends()],
    user_id: Annotated[UUID | None, Depends(get_user_id)],
    movie_id: UUID
):
    if not user_id:
        raise HTTPException(401)
    