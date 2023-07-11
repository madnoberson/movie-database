from abc import ABC, abstractmethod

from src.application.commands.register.command import RegisterCommand, RegisterCommandResult
from src.application.commands.rate_movie.command import RateMovieCommand, RateMovieCommandResult
from src.application.commands.reevaluate_movie.command import (
    ReevaluateMovieCommand, ReevaluateMovieCommandResult
)
from src.application.commands.remove_user_movie_rating.command import (
    RemoveUserMovieRatingCommand, RemoveUserMovieRatingCommandResult
)
from src.application.queries.login.query import LoginQuery, LoginQueryResult
from src.application.queries.username_existence.query import (
    CheckUsernameExistenceQuery, CheckUsernameExistenceQueryResult
)


class TelegramInteractor(ABC):
    
    @abstractmethod
    def handle_register_command(
        self,
        command: RegisterCommand
    ) -> RegisterCommandResult:
        raise NotImplementedError

    @abstractmethod
    def handle_rate_movie_command(
        self,
        command: RateMovieCommand
    ) -> RateMovieCommandResult:
        raise NotImplementedError

    @abstractmethod
    def handle_reevaluate_movie_command(
        self,
        command: ReevaluateMovieCommand
    ) -> ReevaluateMovieCommandResult:
        raise NotImplementedError
    
    @abstractmethod
    def handle_remove_user_movie_rating_command(
        self,
        command: RemoveUserMovieRatingCommand
    ) -> RemoveUserMovieRatingCommandResult:
        raise NotImplementedError

    @abstractmethod
    def handle_login_query(
        self,
        query: LoginQuery
    ) -> LoginQueryResult:
        raise NotImplementedError

    @abstractmethod
    def handle_check_username_existence_query(
        self,
        query: CheckUsernameExistenceQuery
    ) -> CheckUsernameExistenceQueryResult:
        raise NotImplementedError

