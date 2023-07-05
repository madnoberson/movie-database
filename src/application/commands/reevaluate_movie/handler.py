from dataclasses import dataclass
from datetime import datetime

from src.application.common.errors.user import UserDoesNotExistError
from src.application.common.errors.movie import MovieDoesNotExistError
from src.application.common.errors.user_movie_rating import UserMovieRatingDoesNotExistError
from src.domain.models.user.value_objects import UserId
from src.domain.models.movie.value_objects import MovieId
from .command import ReevaluateMovieCommand, ReevaluateMovieCommandResult
from .interfaces import ReevaluateMovieCommandDBGateway


@dataclass(frozen=True, slots=True)
class ReevaluateMovieCommandHandler:

    db_gateway: ReevaluateMovieCommandDBGateway

    def __call__(self, command: ReevaluateMovieCommand) -> ReevaluateMovieCommandResult:
        user_id = UserId(command.user_id)
        user_exists = self.db_gateway.check_user_id_existence(
            user_id=user_id
        )
        if not user_exists:
            raise UserDoesNotExistError(user_id.value)
        
        movie_id = MovieId(command.movie_id)
        movie = self.db_gateway.get_movie_by_id(
            movie_id=movie_id
        )
        if movie is None:
            raise MovieDoesNotExistError(movie_id.value)
        
        umr = self.db_gateway.get_user_movie_rating_by_user_id_and_movie_id(
            user_id=user_id,
            movie_id=movie_id
        )
        if umr is None:
            raise UserMovieRatingDoesNotExistError(movie_id.value)
        
        movie.remove_rating(umr.rating)
        movie.add_rating(command.new_rating)
        self.db_gateway.update_movie(movie)

        umr.update(
            rating=command.new_rating,
            updated_at=datetime.utcnow()
        )
        self.db_gateway.update_user_movie_rating(umr)

        self.db_gateway.commit()

        return ReevaluateMovieCommandResult(
            new_user_rating=command.new_rating,
            new_movie_rating=movie.rating,
            new_movie_rating_count=movie.rating_count
        )
        