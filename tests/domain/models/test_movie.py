from datetime import date
from uuid import uuid4

from src.domain.models.movie.model import Movie
from src.domain.models.movie.value_objects import (
    MovieId, MovieTitle
)


class TestMovie:

    def test_create_should_return_movie(self):
        movie_id = MovieId(uuid4())
        movie_title = MovieTitle("There will be blood")
        movie_release_date = date(2008, 2, 28)

        movie = Movie.create(
            id=movie_id,
            title=movie_title,
            release_date=movie_release_date
        )

        assert movie.id == movie_id
        assert movie.title == movie_title
        assert movie.release_date == movie_release_date
        assert movie.rating == 0
        assert movie.rating_count == 0

    def test_constructor_should_return_movie(self):
        movie_id = MovieId(uuid4())
        movie_title = MovieTitle("There will be blood")
        movie_release_date = date(2008, 2, 28)
        movie_rating = 10
        movie_rating_count = 1

        movie = Movie(
            id=movie_id,
            title=movie_title,
            release_date=movie_release_date,
            rating=movie_rating,
            rating_count=movie_rating_count
        )

        assert movie.id == movie_id
        assert movie.title == movie_title
        assert movie.release_date == movie_release_date
        assert movie.rating == movie_rating
        assert movie.rating_count == movie_rating_count
    
    def test_add_rating_should_add_rating(self):
        movie_id = MovieId(uuid4())
        movie_title = MovieTitle("There will be blood")
        movie_release_date = date(2008, 2, 28)
        movie_rating = 10
        movie_rating_count = 1

        movie = Movie(
            id=movie_id,
            title=movie_title,
            release_date=movie_release_date,
            rating=movie_rating,
            rating_count=movie_rating_count
        )
        movie.add_rating(2)

        assert movie.rating == 6
        assert movie.rating_count == 2

    def test_remove_rating_should_remove_rating(self):
        movie_id = MovieId(uuid4())
        movie_title = MovieTitle("There will be blood")
        movie_release_date = date(2008, 2, 28)
        movie_rating = 6
        movie_rating_count = 2

        movie = Movie(
            id=movie_id,
            title=movie_title,
            release_date=movie_release_date,
            rating=movie_rating,
            rating_count=movie_rating_count
        )
        movie.remove_rating(2)

        assert movie.rating == 10
        assert movie.rating_count == 1