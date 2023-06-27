from abc import abstractmethod
from typing import Protocol

from src.domain.models.user_movie_rating.model import UserMovieRating
from src.domain.models.user.value_objects import UserId
from src.domain.models.movie.value_objects import MovieId


class SupportsSaveUserMovieRating(Protocol):

    @abstractmethod
    def save_user_movie_rating(
        self,
        user_movie_rating: UserMovieRating
    ) -> None:
        raise NotImplementedError
    

class SupportsUpdateUserMovieRating(Protocol):

    @abstractmethod
    def update_user_movie_rating(
        self,
        user_movie_rating: UserMovieRating
    ) -> None:
        raise NotImplementedError


class SupportsGetUserMovieRatingByUserIdAndMovieId(Protocol):

    @abstractmethod
    def get_user_movie_rating_by_user_id_and_movie_id(
        self,
        user_id: UserId,
        movie_id: MovieId
    ) -> UserMovieRating:
        raise NotImplementedError


class SupportsCheckUserMovieRatingExistence(Protocol):

    @abstractmethod
    def check_user_movie_rating_existence(
        self,
        user_id: UserId,
        movie_id: MovieId
    ) -> bool:
        raise NotImplementedError


class SupportsRemoveUserMovieRatingByUserIdAndMovieId(Protocol):

    @abstractmethod
    def remove_user_movie_rating_by_user_id_and_movie_id(
        self,
        user_id: UserId,
        movie_id: MovieId
    ) -> None:
        raise NotImplementedError
    