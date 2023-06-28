import typer

from src.infrastructure.psycopg.psycopg import get_psycopg2_connection
from src.infrastructure.psycopg.gateway import PsycopgDatabaseGateway
from src.infrastructure.password_encoder import HashlibPasswordEncoder
from src.main.ioc import IoC
from .config import PostgresConfig


# FIXME: IoC doesn't have to be created every command call
def interactor_dependency(ctx: typer.Context) -> None:
    if ctx.invoked_subcommand is None:
        return
    
    postgres_config = PostgresConfig()
    psycopg_conn = get_psycopg2_connection(postgres_config)
    db_gateway = PsycopgDatabaseGateway(psycopg_conn)
    password_encoder = HashlibPasswordEncoder()

    ctx.obj = IoC(
        db_gateway=db_gateway,
        password_encoder=password_encoder
    )