from abc import ABC, abstractmethod

from src.application.commands.register.command import (
    RegisterCommand
)
from src.application.commands.register.handler import (
    CommandHandlerResult as RegisterCommandHandlerResult
)
from src.application.commands.rate_movie.command import (
    RateMovieCommand
)
from src.application.commands.rate_movie.handler import (
    CommandHandlerResult as RateMovieCommandHandlerResult
)
from src.application.commands.reevaluate_movie.command import (
    ReevaluateMovieCommand
)
from src.application.commands.reevaluate_movie.handler import(
    CommandHandlerResult as ReevaluateMovieCommandHandlerResult
)
from src.application.commands.remove_user_movie_rating.command import (
    RemoveUserMovieRatingCommand
)
from src.application.commands.remove_user_movie_rating.handler import (
    CommandHandlerResult as RemoveUserMovieRatingCommandHandlerResult
)
from src.application.queries.username_existence.query import (
    CheckUsernameExistenceQuery
)
from src.application.queries.username_existence.handler import (
    QueryHandlerResult as CheckUsernameExistenceQueryHandlerResult
)


class TelegramInteractor(ABC):
    
    @abstractmethod
    def handle_register_command(
        self,
        command: RegisterCommand
    ) -> RegisterCommandHandlerResult:
        raise NotImplementedError

    @abstractmethod
    def handle_rate_movie_command(
        self,
        command: RateMovieCommand
    ) -> RateMovieCommandHandlerResult:
        raise NotImplementedError

    @abstractmethod
    def handle_reevaluate_movie_command(
        self,
        command: ReevaluateMovieCommand
    ) -> ReevaluateMovieCommandHandlerResult:
        raise NotImplementedError
    
    @abstractmethod
    def handle_remove_user_movie_rating_command(
        self,
        command: RemoveUserMovieRatingCommand
    ) -> RemoveUserMovieRatingCommandHandlerResult:
        raise NotImplementedError

    @abstractmethod
    def handle_check_username_existence_query(
        self,
        query: CheckUsernameExistenceQuery
    ) -> CheckUsernameExistenceQueryHandlerResult:
        raise NotImplementedError

