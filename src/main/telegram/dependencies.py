# from aiogram import Dispatcher
# from asyncpg import create_pool

# from src.application.interactors.user.create_user.interactor import CreateUser
# from src.application.interactors.profile.create_profile.interactor import CreateProfile
# from src.application.query_handlers.user.check_email_exists.handler import CheckEmailExists
# from src.application.query_handlers.profile.check_username_exists.handler import CheckUsernameExists
# from src.infrastructure.presentation.common.db_gateway_factory.asyncpg_impl import AsyncpgDatabaseGatewayFactory
# from src.infrastructure.presentation.common.dbq_gateway_factory.asyncpg_impl import AsyncpgDatabaseQueriesGatewayFactory
# from src.infrastructure.application.password_encoder.aiobcrypt_impl import AiobcryptPasswordEncoder
# from src.main.telegram.common.handler_factories import setup_handler_factories
# from .config import PostgresConfig


# async def setup_dependencies(postgres_config: PostgresConfig, dispatcher: Dispatcher) -> None:
#     # 1.Setup interactor factories
#     pool = await create_pool(dsn=postgres_config.dsn)
#     handlers = [CreateUser, CreateProfile, CheckEmailExists, CheckUsernameExists]
#     setup_handler_factories(
#         dispatcher=dispatcher, handlers=handlers,
#         db_gateway_factory=AsyncpgDatabaseGatewayFactory(pool),
#         password_encoder=AiobcryptPasswordEncoder(),
#         dbq_gateway_factory=AsyncpgDatabaseQueriesGatewayFactory(pool)
#     )