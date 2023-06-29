import typer

from src.infrastructure.psycopg.psycopg import get_psycopg2_connection
from src.infrastructure.psycopg.gateway import PsycopgDatabaseGateway
from src.infrastructure.password_encoder import HashlibPasswordEncoder
from src.main.cli
from .config import PostgresConfig


def interactor_callback(ctx: typer.Context) -> None:
    if ctx.invoked_subcommand is None:
        return
    
    postgres_config = PostgresConfig()
    psycopg_conn = get_psycopg2_connection(postgres_config.dsn)

    db_gateway = PsycopgDatabaseGateway(psycopg_conn)
    password_encoder = HashlibPasswordEncoder()

    ioc = IoC(
        db_gateway=db_gateway,
        password_encoder=password_encoder
    )
    ctx.obj = ioc


def create_app() -> typer.Typer:
    app = typer.Typer(callback=interactor_callback)

    return app
