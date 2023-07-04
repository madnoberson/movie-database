from pydantic import BaseSettings


class PostgresConfig(BaseSettings):

    postgres_host: str = "127.0.0.1"
    postgres_port: str = 5432
    postgres_name: str = "movie_database"
    postgres_user: str = "postgres"
    postgres_password: str = 1234

    @property
    def dsn(self) -> str:
        dsn = "postgresql://{}:{}@{}:{}/{}".format(
            self.postgres_user,
            self.postgres_password,
            self.postgres_host,
            self.postgres_port,
            self.postgres_name
        )
        return dsn


class YandexObjectStorageConfig(BaseSettings):

    yandex_os_access_key_id: str = "YCAJEdiDDYMhmN0YI1jYIQayk"
    yandex_os_access_key: str
    yandex_os_region_name: str = "ru-central1"
    yandex_os_endpoint_url: str = "https://storage.yandexcloud.net"

    yandex_os_image_bucket: str = "movie-database"


class TelegramConfig(BaseSettings):

    telegram_bot_token: str


class Config:

    telegram: TelegramConfig = TelegramConfig()
    postgres: PostgresConfig = PostgresConfig()
    yandex_os: YandexObjectStorageConfig = YandexObjectStorageConfig()