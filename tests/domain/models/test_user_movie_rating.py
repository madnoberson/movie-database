from datetime import datetime
from uuid import uuid4

from src.domain.models.user.value_objects import UserId
from src.domain.models.movie.value_objects import MovieId
from src.domain.models.user_movie_rating.model import (
    UserMovieRating
)


class TestUserMovieRating:
    
    def test_create_should_return_user_movie_rating(self):
        user_id = UserId(uuid4())
        movie_id = MovieId(uuid4())
        rating = 10
        created_at = datetime.utcnow()

        user_movie_rating = UserMovieRating.create(
            user_id=user_id,
            movie_id=movie_id,
            rating=rating,
            created_at=created_at
        )

        assert user_movie_rating.user_id == user_id
        assert user_movie_rating.movie_id == movie_id
        assert user_movie_rating.rating == rating
        assert user_movie_rating.created_at == created_at
        assert user_movie_rating.updated_at == None
    
    def test_constructor_should_return_user_movie_rating(self):
        user_id = UserId(uuid4())
        movie_id = MovieId(uuid4())
        rating = 10
        created_at = datetime.utcnow()
        updated_at = None

        user_movie_rating = UserMovieRating(
            user_id=user_id,
            movie_id=movie_id,
            rating=rating,
            created_at=created_at,
            updated_at=updated_at
        )

        assert user_movie_rating.user_id == user_id
        assert user_movie_rating.movie_id == movie_id
        assert user_movie_rating.rating == rating
        assert user_movie_rating.created_at == created_at
        assert user_movie_rating.updated_at == updated_at
