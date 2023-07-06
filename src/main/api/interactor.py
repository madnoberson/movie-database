from dataclasses import dataclass

from src.presentation.api.interactor import ApiInteractor
from src.application.common.interfaces.database_gateway import DatabaseGateway
from src.application.common.interfaces.passoword_encoder import PasswordEncoder
from src.application.commands.register.command import (
    RegisterCommand, RegisterCommandResult
)
from src.application.commands.register.handler import RegisterCommandHandler
from src.application.commands.rate_movie.command import (
    RateMovieCommand, RateMovieCommandResult
)
from src.application.commands.rate_movie.handler import RateMovieCommandHandler
from src.application.commands.reevaluate_movie.command import (
    ReevaluateMovieCommand, ReevaluateMovieCommandResult
)
from src.application.commands.reevaluate_movie.handler import ReevaluateMovieCommandHandler
from src.application.commands.remove_user_movie_rating.command import (
    RemoveUserMovieRatingCommand, RemoveUserMovieRatingCommandResult
)
from src.application.commands.remove_user_movie_rating.handler import (
    RemoveUserMovieRatingCommandHandler
)
from src.application.queries.login.query import LoginQuery, LoginQueryResult
from src.application.queries.login.handler import LoginQueryHandler
from src.application.queries.username_existence.query import (
    CheckUsernameExistenceQuery, CheckUsernameExistenceQueryResult
)
from src.application.queries.username_existence.handler import (
    CheckUsernameExistenceQueryHandler
)


@dataclass(frozen=True, slots=True)
class ApiInteractorImpl(ApiInteractor):

    db_gateway: DatabaseGateway
    password_encoder: PasswordEncoder

    def handle_register_command(
        self,
        command: RegisterCommand
    ) -> RegisterCommandResult:
        handler = RegisterCommandHandler(
            db_gateway=self.db_gateway,
            password_encoder=self.password_encoder
        )
        return handler(command)

    def handle_rate_movie_command(
        self,
        command: RateMovieCommand
    ) -> RateMovieCommandResult:
        handler = RateMovieCommandHandler(
            db_gateway=self.db_gateway
        )
        return handler(command)
    
    def handle_reevaluate_movie_command(
        self,
        command: ReevaluateMovieCommand
    ) -> ReevaluateMovieCommandResult:
        handler = ReevaluateMovieCommandHandler(
            db_gateway=self.db_gateway
        )
        return handler(command)
    
    def handle_remove_user_movie_rating_command(
        self,
        command: RemoveUserMovieRatingCommand
    ) -> RemoveUserMovieRatingCommandResult:
        handler = RemoveUserMovieRatingCommandHandler(
            db_gateway=self.db_gateway
        )
        return handler(command)

    def handle_login_query(
        self,
        query: LoginQuery
    ) -> LoginQueryResult:
        handler = LoginQueryHandler(
            db_gateway=self.db_gateway,
            password_encoder=self.password_encoder
        )
        return handler(query)

    def handle_check_username_existence_query(
        self,
        query: CheckUsernameExistenceQuery
    ) -> CheckUsernameExistenceQueryResult:
        hanlder = CheckUsernameExistenceQueryHandler(
            db_gateway=self.db_gateway
        )
        return hanlder(query)
    