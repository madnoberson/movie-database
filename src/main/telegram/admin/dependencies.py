from aiogram import Dispatcher
from asyncpg import create_pool

from src.application.interactors.user.create_user.interactor import CreateUser
from src.application.interactors.profile.create_profile.interactor import CreateProfile
from src.application.interactors.queries.user.check_email_exists.interactor import CheckEmailExists
from src.application.interactors.queries.profile.check_username_exists.interactor import CheckUsernameExists
from src.infrastructure.presentation.common.db_gateway_factory.asyncpg_impl import AsyncpgDatabaseGatewayFactory
from src.infrastructure.application.password_encoder.aiobcrypt_impl import AiobcryptPasswordEncoder
from src.main.telegram.common.interactor_factories import setup_interactor_factories
from .config import PostgresConfig


async def setup_dependencies(postgres_config: PostgresConfig, dispatcher: Dispatcher) -> None:
    # 1.Setup interactor factories
    pool = await create_pool(dsn=postgres_config.dsn)
    interactors = [CreateUser, CreateProfile, CheckEmailExists, CheckUsernameExists]
    setup_interactor_factories(
        dispatcher=dispatcher, interactors=interactors,
        db_gateway_factory=AsyncpgDatabaseGatewayFactory(pool),
        password_encoder=AiobcryptPasswordEncoder()
    )

