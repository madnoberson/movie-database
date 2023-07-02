from uuid import uuid4

from src.domain.models.movie.value_objects import MovieId
from src.domain.models.movie_genres.model import MovieGenres
from src.domain.models.movie_genres.constants import MovieGenreEnum


class TestMovieGenres:

    def test_create_should_return_movie_genres(self):
        movie_id = MovieId(uuid4())
        genres = [MovieGenreEnum(1), MovieGenreEnum(10)]

        movie_genres = MovieGenres.create(
            movie_id=movie_id,
            genres=genres
        )

        assert movie_genres.movie_id == movie_id
        assert movie_genres.genres == genres

    def test_constructor_should_return_movie_genres(self):
        movie_id = MovieId(uuid4())
        genres = [MovieGenreEnum(1), MovieGenreEnum(10)]

        movie_genres = MovieGenres(
            movie_id=movie_id,
            genres=genres
        )

        assert movie_genres.movie_id == movie_id
        assert movie_genres.genres == genres
