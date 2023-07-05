from dataclasses import dataclass, field
from datetime import datetime, date
from uuid import uuid4

import pytest

from src.application.common.errors.user import UserDoesNotExistError
from src.application.common.errors.movie import MovieDoesNotExistError
from src.application.common.errors.user_movie_rating import (
    UserMovieRatingDoesNotExistError
)
from src.domain.models.user.model import User
from src.domain.models.user.value_objects import UserId, Username
from src.domain.models.movie.model import Movie
from src.domain.models.movie.value_objects import MovieId, MovieTitle
from src.domain.models.user_movie_rating.model import UserMovieRating
from src.application.commands.reevaluate_movie.command import (
    ReevaluateMovieCommand,
    ReevaluateMovieCommandResult
)
from src.application.commands.reevaluate_movie.handler import (
    ReevaluateMovieCommandHandler
)
from src.application.commands.reevaluate_movie.interfaces import (
    ReevaluateMovieCommandDBGateway
)


@dataclass(frozen=True, slots=True)
class FakeReevaluateMovieCommandDBGateway(
    ReevaluateMovieCommandDBGateway
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
    
    def update_user_movie_rating(
        self,
        user_movie_rating: UserMovieRating
    ) -> None:
        user_id = user_movie_rating.user_id
        movie_id = user_movie_rating.movie_id
        self.user_movie_ratings[(user_id, movie_id)] = user_movie_rating
    
    def commit(self) -> None:
        ...
    
    def rollback(self) -> None:
        ...


class TestReevaluateMovieCommand:

    def test_valid_args(self):
        try:
            ReevaluateMovieCommand(
                user_id=uuid4(),
                movie_id=uuid4(),
                new_rating=10
            )
            ReevaluateMovieCommand(
                user_id=uuid4(),
                movie_id=uuid4(),
                new_rating=5.5
            )
        except ValueError:
            pytest.fail()
    
    def test_invalid_args(self):
        with pytest.raises(ValueError):
            ReevaluateMovieCommand(
                user_id=1,
                movie_id=uuid4(),
                new_rating=10
            )
            ReevaluateMovieCommand(
                user_id=uuid4(),
                movie_id=1,
                new_rating=10
            )
            ReevaluateMovieCommand(
                user_id=uuid4(),
                movie_id=uuid4(),
                new_rating=12
            )
            ReevaluateMovieCommand(
                user_id=uuid4(),
                movie_id=uuid4(),
                new_rating=0
            )
            ReevaluateMovieCommand(
                user_id=uuid4(),
                movie_id=uuid4(),
                new_rating=6.6
            )


class TestReevaluateMovieCommandHandler:

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
            rating=5,
            rating_count=1
        )
        movies = {movie.id: movie}
        
        umr = UserMovieRating(
            user_id=user.id,
            movie_id=movie.id,
            rating=5,
            created_at=datetime.utcnow(),
            updated_at=None
        )
        user_movie_ratings = {(umr.user_id, umr.movie_id): umr}

        db_gateway = FakeReevaluateMovieCommandDBGateway(
            users=users,
            movies=movies,
            user_movie_ratings=user_movie_ratings
        )
        handler = ReevaluateMovieCommandHandler(db_gateway)

        command = ReevaluateMovieCommand(
            user_id=user.id.value,
            movie_id=movie.id.value,
            new_rating=10
        )

        try:
            result = handler(command)
        except (
            UserDoesNotExistError,
            MovieDoesNotExistError,
            UserMovieRatingDoesNotExistError
        ) as e:
            pytest.fail(reason=str(e))
        
        assert isinstance(result, ReevaluateMovieCommandResult)
        assert result.new_movie_rating == 10
        assert result.new_user_rating == 10
    
    def test_handler_should_raise_error_when_user_does_not_exist(self):
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

        db_gateway = FakeReevaluateMovieCommandDBGateway(
            movies=movies,
            user_movie_ratings=user_movie_ratings
        )
        handler = ReevaluateMovieCommandHandler(db_gateway)

        command = ReevaluateMovieCommand(
            user_id=uuid4(),
            movie_id=movie.id.value,
            new_rating=10
        )

        with pytest.raises(UserDoesNotExistError) as e:
            handler(command)

        assert e.value == UserDoesNotExistError(command.user_id)
    
    def test_handler_should_raise_error_when_movie_does_not_exist(self):
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

        db_gateway = FakeReevaluateMovieCommandDBGateway(
            users=users,
            user_movie_ratings=user_movie_ratings
        )
        handler = ReevaluateMovieCommandHandler(db_gateway)

        command = ReevaluateMovieCommand(
            user_id=user.id.value,
            movie_id=uuid4(),
            new_rating=10
        )

        with pytest.raises(MovieDoesNotExistError) as e:
            handler(command)

        assert e.value == MovieDoesNotExistError(command.movie_id)
    
    def test_handler_should_raise_error_when_umr_does_not_exist(self):
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

        db_gateway = FakeReevaluateMovieCommandDBGateway(
            users=users,
            movies=movies
        )
        handler = ReevaluateMovieCommandHandler(db_gateway)

        command = ReevaluateMovieCommand(
            user_id=user.id.value,
            movie_id=movie.id.value,
            new_rating=10
        )
        
        with pytest.raises(UserMovieRatingDoesNotExistError) as e:
            handler(command)

        assert e.value == UserMovieRatingDoesNotExistError(command.movie_id)