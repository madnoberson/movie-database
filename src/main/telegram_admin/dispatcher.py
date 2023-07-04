from aiogram import Dispatcher
import boto3

from src.infrastructure.psycopg.psycopg import get_psycopg2_connection
from src.infrastructure.psycopg.gateway import PsycopgDatabaseGateway
from src.infrastructure.yandex_os.gateway import YandexOSFilebaseGateway
from src.presentation.telegram_admin.movies import movies_router
from .interactor import TelegramAdminInteractorImpl
from .middlewares import TelegramInteractorMiddleware
from .config import PostgresConfig, YandexObjectStorageConfig


def create_dispatcher(
    postgres_config: PostgresConfig,
    yandex_os_config: YandexObjectStorageConfig
) -> Dispatcher:
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

    dp = Dispatcher()
    dp.include_router(movies_router)
    dp.message.middleware(interactor_middleware)

    return dp

