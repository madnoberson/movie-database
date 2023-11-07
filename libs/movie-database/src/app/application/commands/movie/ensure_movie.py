from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from app.domain.models.movie import Movie
from app.application.common.interfaces.uow import UnitOfWork
from app.application.common.interfaces import repositories
from app.application.commands.handler import CommandHandler


@dataclass(frozen=True, slots=True)
class InputDTO:

    movie_id: UUID
    en_name: str
    created_at: datetime


class EnsureMovie(CommandHandler):

    def __init__(
        self,
        movie_repo: repositories.MovieRepository,
        uow: UnitOfWork
    ) -> None:
        self.movie_repo = movie_repo
        self.uow = uow
    
    async def __call__(self, data: InputDTO) -> None:
        # 1.Check if movie already exists
        if await self.movie_repo.check_movie_exists(
            movie_id=data.movie_id
        ):
            return
        
        # 2.Create movie
        movie = Movie.create(
            movie_id=data.movie_id, en_name=data.en_name,
            created_at=data.created_at
        )
        await self.movie_repo.save_movie(movie)

        await self.uow.commit()