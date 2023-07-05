from aiogram import Dispatcher
import boto3

from src.infrastructure.psycopg.psycopg import get_psycopg2_connection
from src.infrastructure.psycopg.gateway import PsycopgDatabaseGateway
from src.infrastructure.yandex_os.gateway import YandexOSFilebaseGateway
from src.presentation.telegram_admin.add_movie import create_add_movie_router
from src.presentation.telegram_admin.remove_movie import create_remove_movie_router
from .interactor import TelegramAdminInteractorImpl
from .middlewares import TelegramInteractorMiddleware
from .config import PostgresConfig, YandexObjectStorageConfig


def setup_routes(dp: Dispatcher) -> None:
    add_movie_router = create_add_movie_router()
    dp.include_router(add_movie_router)

    remove_movie_router = create_remove_movie_router()
    dp.include_router(remove_movie_router)


def setup_middlewares(
    dp: Dispatcher,
    postgres_config: PostgresConfig,
    yandex_os_config: YandexObjectStorageConfig
) -> None:
    psycopg_conn = get_psycopg2_connection(postgres_config.dsn)
    db_gateway = PsycopgDatabaseGateway(psycopg_conn)

    boto3_client = boto3.client(
        "s3",
        aws_access_key_id=yandex_os_config.yandex_os_access_key_id,
        aws_secret_access_key=yandex_os_config.yandex_os_access_key,
        region_name=yandex_os_config.yandex_os_region_name,
        endpoint_url=yandex_os_config.yandex_os_endpoint_url
    )
    fb_gateway = YandexOSFilebaseGateway(
        image_bucket=yandex_os_config.yandex_os_image_bucket,
        boto3_client=boto3_client
    )

    interactor = TelegramAdminInteractorImpl(
        db_gateway=db_gateway,
        fb_gateway=fb_gateway
    )
    interactor_middleware = TelegramInteractorMiddleware(
        interactor=interactor
    )

    dp.message.middleware.register(interactor_middleware)


def create_dispatcher(
    postgres_config: PostgresConfig,
    yandex_os_config: YandexObjectStorageConfig
) -> Dispatcher:
    dispatcher = Dispatcher()

    setup_routes(
        dp=dispatcher
    )
    setup_middlewares(
        dp=dispatcher,
        postgres_config=postgres_config,
        yandex_os_config=yandex_os_config
    )

    return dispatcher

