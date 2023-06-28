from aiogram import Dispatcher

from src.infrastructure.psycopg.psycopg import get_psycopg2_connection
from src.infrastructure.psycopg.gateway import PsycopgDatabaseGateway
from src.infrastructure.password_encoder import HashlibPasswordEncoder
from src.main.ioc import IoC
from src.presentation.telegram.auth.handlers import auth_router
from .middlewares import IoCMiddleware
from .config import PostgresConfig



def create_dipatcher(postgres_config: PostgresConfig) -> Dispatcher:
    psycopg_conn = get_psycopg2_connection(postgres_config.dsn)

    db_gateway = PsycopgDatabaseGateway(psycopg_conn)
    password_encoder = HashlibPasswordEncoder()

    ioc = IoC(
        db_gateway=db_gateway,
        password_encoder=password_encoder
    )
    ioc_middleware = IoCMiddleware(ioc)

    dp = Dispatcher()

    dp.message.middleware(ioc_middleware)
    dp.include_router(auth_router)
    
    return dp

