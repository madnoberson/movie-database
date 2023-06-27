from dataclasses import dataclass, field
from datetime import datetime, date
from uuid import uuid4

import pytest

from src.application.common.result import Result
from src.application.common.errors.user import (
    UserDoesNotExistError
)
from src.application.common.errors.movie import (
    MovieDoesNotExistError
)
from src.application.common.errors.user_movie_rating import (
    UserMovieRatingDoesNotExistError
)
from src.domain.models.user.model import User
from src.domain.models.user.value_objects import (
    UserId, Username
)
from src.domain.models.movie.model import Movie
from src.domain.models.movie.value_objects import (
    MovieId, MovieTitle
)
from src.domain.models.user_movie_rating.model import (
    UserMovieRating
)
from src.application.commands.remove_user_movie_rating.command import (
    RemoveUserMovieRatingCommand
)
from src.application.commands.remove_user_movie_rating.handler import (
    RemoveUserMovieRatingCommandHandler
)
from src.application.commands.remove_user_movie_rating.interfaces import (
    RemoveUserMovieRatingCommandDBGateway
)


@dataclass(frozen=True, slots=True)
class FakeRemoveUserMovieRatingCommandDBGateway(
    RemoveUserMovieRatingCommandDBGateway
):
    users: dict[UserId, User] = field(
        default_factory=dict
    )
    movies: dict[MovieId, Movie] = field(
        default_factory=dict
    )
    user_movie_ratings: dict[
        (UserId, MovieId), UserMovieRating
    ] = field(default_factory=dict)

    def check_user_id_existence(
        self,
        user_id: UserId
    ) -> bool:
        return not self.users.get(user_id) is None

    def get_movie_by_id(
        self,
        movie_id: MovieId
    ) -> Movie | None:
        return self.movies.get(movie_id)

    def update_movie(
        self,
        movie: Movie
    ) -> None:
        self.movies[movie.id] = movie
    
    def get_user_movie_rating_by_user_id_and_movie_id(
        self,
        user_id: UserId,
        movie_id: MovieId
    ) -> UserMovieRating:
        return self.user_movie_ratings.get((user_id, movie_id))

    def remove_user_movie_rating_by_user_id_and_movie_id(
        self,
        user_id: UserId,
        movie_id: MovieId
    ) -> None:
        self.user_movie_ratings.pop((user_id, movie_id))

    def commit(self) -> None:
        ...
    
    def rollback(self) -> None:
        ...


class TestRemoveUserMovieCommand:


    def test_valid_args(self):
        try:
            RemoveUserMovieRatingCommand(
                user_id=uuid4(),
                movie_id=uuid4()
            )
        except ValueError:
            pytest.fail()
    
    def test_invalid_args(self):
        with pytest.raises(ValueError):
            RemoveUserMovieRatingCommand(
                user_id=1,
                movie_id=uuid4()
            )
            RemoveUserMovieRatingCommand(
                user_id=uuid4(),
                movie_id=1
            )


class TestRemoveUserMovieCommandHandler:

    db_gateway: RemoveUserMovieRatingCommandDBGateway

    def test_handler_should_return_normal_result(self):
        user = User(
            id=UserId(uuid4()),
            username=Username("johndoe"),
            password="encodedpassword",
            created_at=datetime.utcnow()
        )
        users = {user.id: user}

        movie = Movie(
            id=MovieId(uuid4()),
            title=MovieTitle("There will be blood"),
            release_date=date.today(),
            rating=0,
            rating_count=0
        )
        movies = {movie.id: movie}
        
        umr = UserMovieRating(
            user_id=user.id,
            movie_id=movie.id,
            rating=10,
            created_at=datetime.utcnow(),
            updated_at=None
        )
        user_movie_ratings = {(umr.user_id, umr.movie_id): umr}

        db_gateway = FakeRemoveUserMovieRatingCommandDBGateway(
            users=users,
            movies=movies,
            user_movie_ratings=user_movie_ratings
        )
        handler = RemoveUserMovieRatingCommandHandler(db_gateway)

        command = RemoveUserMovieRatingCommand(
            user_id=user.id.value,
            movie_id=movie.id.value
        )
        result = handler(command)

        assert result == Result(None, None)
    
    def test_handler_should_return_error_when_user_does_not_exist(self):
        movie = Movie(
            id=MovieId(uuid4()),
            title=MovieTitle("There will be blood"),
            release_date=date.today(),
            rating=0,
            rating_count=0
        )
        movies = {movie.id: movie}
        
        umr = UserMovieRating(
            user_id=UserId(uuid4()),
            movie_id=movie.id,
            rating=10,
            created_at=datetime.utcnow(),
            updated_at=None
        )
        user_movie_ratings = {(umr.user_id, umr.movie_id): umr}

        db_gateway = FakeRemoveUserMovieRatingCommandDBGateway(
            movies=movies,
            user_movie_ratings=user_movie_ratings
        )
        handler = RemoveUserMovieRatingCommandHandler(db_gateway)

        command = RemoveUserMovieRatingCommand(
            user_id=uuid4(),
            movie_id=movie.id.value
        )
        result = handler(command)

        assert result.value == None
        assert result.error == UserDoesNotExistError(command.user_id)
    
    def test_handler_should_return_error_when_movie_does_not_exist(self):
        user = User(
            id=UserId(uuid4()),
            username=Username("johndoe"),
            password="encodedpassword",
            created_at=datetime.utcnow()
        )
        users = {user.id: user}

        umr = UserMovieRating(
            user_id=user.id,
            movie_id=MovieId(uuid4()),
            rating=10,
            created_at=datetime.utcnow(),
            updated_at=None
        )
        user_movie_ratings = {(umr.user_id, umr.movie_id): umr}

        db_gateway = FakeRemoveUserMovieRatingCommandDBGateway(
            users=users,
            user_movie_ratings=user_movie_ratings
        )
        handler = RemoveUserMovieRatingCommandHandler(db_gateway)

        command = RemoveUserMovieRatingCommand(
            user_id=user.id.value,
            movie_id=uuid4()
        )
        result = handler(command)

        assert result.value == None
        assert result.error == MovieDoesNotExistError(command.movie_id)
    
    def test_handler_should_return_error_when_umr_does_not_exist(self):
        user = User(
            id=UserId(uuid4()),
            username=Username("johndoe"),
            password="encodedpassword",
            created_at=datetime.utcnow()
        )
        users = {user.id: user}

        movie = Movie(
            id=MovieId(uuid4()),
            title=MovieTitle("There will be blood"),
            release_date=date.today(),
            rating=0,
            rating_count=0
        )
        movies = {movie.id: movie}
        

        db_gateway = FakeRemoveUserMovieRatingCommandDBGateway(
            users=users,
            movies=movies
        )
        handler = RemoveUserMovieRatingCommandHandler(db_gateway)

        command = RemoveUserMovieRatingCommand(
            user_id=user.id.value,
            movie_id=movie.id.value
        )
        result = handler(command)

        assert result.value == None
        assert result.error == UserMovieRatingDoesNotExistError(movie.id.value)
