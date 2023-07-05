from dataclasses import dataclass

from src.application.common.errors.movie import MovieDoesNotExistError
from src.domain.models.movie.value_objects import MovieId
from .command import RemoveMovieCommand
from .interfaces import RemoveMovieCommandDBGateway, RemoveMovieCommandFBGateway


@dataclass(frozen=True, slots=True)
class RemoveMovieCommandHandler:
    """
    Raises:
        * `MovieDoesNotExistError` \n   
    Returns:
        * `None` 
    """

    db_gateway: RemoveMovieCommandDBGateway
    fb_gateway: RemoveMovieCommandFBGateway

    def __call__(self, command: RemoveMovieCommand) -> None:
        movie_id = MovieId(command.movie_id)

        movie_exists = self.db_gateway.check_movie_existence_by_id(
            movie_id=movie_id
        )
        if not movie_exists:
            raise MovieDoesNotExistError(movie_id.value)
        
        self.db_gateway.remove_movie_by_id(movie_id.value)
        self.db_gateway.commit()

        # TODO: Remove movie poster
        # self.fb_gateway.remove_movie_poster()
