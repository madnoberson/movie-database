from dataclasses import dataclass
from datetime import datetime
from uuid import UUID, uuid4

from app.domain.models.movie import Movie
from app.application.common.handler import CommandHandler
from app.application.common.interfaces.repositories import MovieRepository
from app.application.common.protocols.uow import UnitOfWork


@dataclass(frozen=True, slots=True)
class InputDTO:

    title: str


@dataclass(frozen=True, slots=True)
class OutputDTO:

    movie_id: UUID


class CreateMovie(CommandHandler):

    def __init__(self, movie_repo: MovieRepository, uow: UnitOfWork) -> None:
        self.movie_repo = movie_repo
        self.uow = uow
    
    async def __call__(self, data: InputDTO) -> OutputDTO:
        # 1.Create movie
        movie = Movie.create(movie_id=uuid4(), title=data.title, created_at=datetime.utcnow())

        # 2.Save movie
        await self.movie_repo.save_movie(movie)
        await self.uow.commit()

        return OutputDTO(movie_id=movie.id)