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


class TelegramConfig(BaseSettings):

    telegram_bot_token: str


class Config:

    telegram: TelegramConfig = TelegramConfig()
    postgres: PostgresConfig = PostgresConfig()