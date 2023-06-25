from dataclasses import dataclass, field
from datetime import datetime, date
from uuid import uuid4

from src.application.common.result import Result
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
from src.application.common.errors.user import (
    UserDoesNotExistError
)
from src.application.common.errors.movie import (
    MovieDoesNotExistError
)
from src.application.commands.rate_movie.command import (
    RateMovieCommand,
    RateMovieCommandResult
)
from src.application.commands.rate_movie.handler import (
    RateMovieCommandHandler
)
from src.application.commands.rate_movie.interfaces import (
    RateMovieDBGateway
)
from src.application.commands.rate_movie.errors import (
    UserMovieRatingAlreadyExistsError
)


@dataclass(frozen=True, slots=True)
class FakeRateMovieDBGateway(RateMovieDBGateway):

    users: dict[UserId, User] = field(
        default_factory=dict
    )
    movies: dict[MovieId, Movie] = field(
        default_factory=dict
    )
    user_movie_ratings: dict[
        (UserId, MovieId), UserMovieRating
    ] = field(default_factory=dict)

    def check_user_id_existence(self, user_id: UserId) -> bool:
        return not self.users.get(user_id) is None

    def get_movie_by_id(self, movie_id: MovieId) -> Movie | None:
        return self.movies.get(movie_id)

    def update_movie(self, movie: Movie) -> None:
        self.movies[movie.id] = movie

    def save_user_movie_rating(
        self,
        user_movie_rating: UserMovieRating
    ) -> None:
        user_id = user_movie_rating.user_id
        movie_id = user_movie_rating.movie_id
        self.user_movie_ratings[(user_id, movie_id)] = user_movie_rating

    def check_user_movie_rating_existence(
        self,
        user_id: UserId,
        movie_id: MovieId
    ) -> bool:
        return not self.user_movie_ratings.get((user_id, movie_id)) is None

    def commit(self) -> None:
        ...
    
    def rollback(self) -> None:
        ...


class TestRateMovieCommand:

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
        
        db_gateway = FakeRateMovieDBGateway(
            users=users,
            movies=movies
        )
        handler = RateMovieCommandHandler(db_gateway)
        
        command = RateMovieCommand(
            user_id=user.id.value,
            movie_id=movie.id.value,
            rating=10
        )
        result: Result = handler(command)

        assert result.error == None
        assert isinstance(result.value, RateMovieCommandResult)
        assert result.value.new_movie_rating == 10
        assert result.value.user_rating == 10
        assert result.value.new_movie_rating_count == 1
    
    def test_handler_should_return_error_when_user_does_not_exist(self):
        handler = RateMovieCommandHandler(
            db_gateway=FakeRateMovieDBGateway()
        )
        
        user_id = UserId(uuid4())
        command = RateMovieCommand(
            user_id=user_id.value,
            movie_id=MovieId(uuid4()).value,
            rating=10
        )
        result: Result = handler(command)

        assert result.value == None
        assert result.error == UserDoesNotExistError(user_id.value)
    
    def test_handler_should_return_error_when_movie_does_not_exist(self):
        user = User(
            id=UserId(uuid4()),
            username=Username("johndoe"),
            password="encodedpassword",
            created_at=datetime.utcnow()
        )
        users = {user.id: user}

        handler = RateMovieCommandHandler(
            db_gateway=FakeRateMovieDBGateway(users)
        )

        movie_id = MovieId(uuid4())
        command = RateMovieCommand(
            user_id=user.id.value,
            movie_id=movie_id.value,
            rating=10
        )
        result: Result = handler(command)

        assert result.value == None
        assert result.error == MovieDoesNotExistError(movie_id.value)
    
    def test_handler_should_return_error_when_umr_already_exists(self):
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

        db_gateway = FakeRateMovieDBGateway(
            users=users,
            movies=movies,
            user_movie_ratings=user_movie_ratings
        )
        handler = RateMovieCommandHandler(db_gateway)

        command = RateMovieCommand(
            user_id=user.id.value,
            movie_id=movie.id.value,
            rating=10
        )
        result: Result = handler(command)

        assert result.value == None
        assert result.error == UserMovieRatingAlreadyExistsError(movie.id.value)