from aiogram import Dispatcher

from src.infrastructure.psycopg.psycopg import get_psycopg2_connection
from src.infrastructure.psycopg.gateway import PsycopgDatabaseGateway
from src.infrastructure.password_encoder import HashlibPasswordEncoder
from src.main.ioc import IoC


def create_dipatcher() -> Dispatcher:
    psycopg_conn = get_psycopg2_connection()

    db_gateway = PsycopgDatabaseGateway(psycopg_conn)
    password_encoder = HashlibPasswordEncoder()

    ioc = IoC(
        db_gateway=db_gateway,
        password_encoder=password_encoder
    )
    dp = Dispatcher(ioc=ioc)
    
    return dp

