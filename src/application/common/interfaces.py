from abc import ABC, abstractmethod

from src.domain.models.movie.model import Movie
from src.domain.models.movie.value_objects import MovieId
from src.domain.models.user.model import User
from src.domain.models.user.value_objects import UserId, Username


class Atomic(ABC):
    
    @abstractmethod
    def commit(self) -> None:
        raise NotImplementedError
    
    @abstractmethod
    def rollback(self) -> None:
        raise NotImplementedError


class UserReader(ABC):

    @abstractmethod
    def get_user_by_id(self, user_id: UserId) -> User | None:
        raise NotImplementedError

    @abstractmethod
    def get_user_by_username(self, username: Username) -> User | None:
        raise NotImplementedError


class UserSaver(ABC):

    @abstractmethod
    def save_user(self, user: User) -> None:
        raise NotImplementedError


class MovieReader(ABC):

    @abstractmethod
    def get_movie_by_id(self, movie_id: MovieId) -> Movie | None:
        raise NotImplementedError


class MovieSaver(ABC):

    @abstractmethod
    def save_movie(self, movie: Movie) -> None:
        raise NotImplementedError

