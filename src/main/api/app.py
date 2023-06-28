from fastapi import FastAPI

from src.presentation.interactor import Interactor
from src.presentation.api.authenticator import ApiAuthenticator
from src.presentation.api.auth.routes import auth_router
from src.main.ioc import IoC
from src.infrastructure.psycopg.psycopg import get_psycopg2_connection
from src.infrastructure.psycopg.gateway import PsycopgDatabaseGateway
from src.infrastructure.password_encoder import HashlibPasswordEncoder
from src.infrastructure.auth.api import ApiAuthenticatorImpl
from .config import Config, AuthConfig, PostgresConfig


def setup_providers(
    app: FastAPI,
    auth_config: AuthConfig,
    postgres_config: PostgresConfig
) -> None:
    psycopg_conn = get_psycopg2_connection(postgres_config.dsn)
    psycopg_db_gateway = PsycopgDatabaseGateway(psycopg_conn)
    password_encoder = HashlibPasswordEncoder()

    ioc = IoC(
        db_gateway=psycopg_db_gateway,
        password_encoder=password_encoder
    )
    authenticator = ApiAuthenticatorImpl(
        secret=auth_config.auth_secret,
        access_token_expires=auth_config.auth_access_token_expires,
        refresh_token_expires=auth_config.auth_refresh_token_expires,
        algorithm=auth_config.auth_algorithm
    )

    app.dependency_overrides[Interactor] = lambda: ioc
    app.dependency_overrides[ApiAuthenticator] = lambda: authenticator



def setup_routers(app: FastAPI) -> None:
    app.include_router(auth_router)


def create_app(config: Config) -> FastAPI:
    app = FastAPI(
        title=config.fastapi.fastapi_title,
        description=config.fastapi.fastapi_description,
        version=config.fastapi.fastapi_version
    )

    setup_providers(
        app=app,
        auth_config=config.auth,
        postgres_config=config.postgres
    )
    setup_routers(app)

    return app
