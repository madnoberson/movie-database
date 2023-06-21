from fastapi import FastAPI

from src.presentation.interactor_factory import InteractorFactory
from src.presentation.api.authenticator import ApiAuthenticator
from src.presentation.api.auth.routes import auth_router
from src.main.ioc import IoC
from src.infrastructure.psycopg.psycopg import build_psycopg2_connection
from src.infrastructure.psycopg.gateway import PsycopgDatabaseGateway
from src.infrastructure.password_encoder import HashlibPasswordEncoder
from src.infrastructure.auth.api import ApiAuthenticatorImpl
from .config import Config, AuthConfig


def setup_providers(app: FastAPI, auth_config: AuthConfig) -> None:
    psycopg_conn = build_psycopg2_connection()
    psycopg_db_gateway = PsycopgDatabaseGateway(psycopg_conn)
    password_encoder = HashlibPasswordEncoder()

    ioc = IoC(
        db_gateway=psycopg_db_gateway,
        password_encoder=password_encoder
    )

    authenticator = ApiAuthenticatorImpl(
        secret=auth_config.secret,
        access_token_expires=auth_config.access_token_expires,
        refresh_token_expires=auth_config.refresh_token_expires,
        algorithm=auth_config.algorithm
    )

    app.dependency_overrides[InteractorFactory] = lambda: ioc
    app.dependency_overrides[ApiAuthenticator] = lambda: authenticator



def setup_routers(app: FastAPI) -> None:
    app.include_router(auth_router)


def create_app(config: Config) -> FastAPI:
    app = FastAPI(
        title=config.fastapi.title,
        description=config.fastapi.description,
        version=config.fastapi.version
    )

    setup_providers(app, config.auth)
    setup_routers(app)

    return app
