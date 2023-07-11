from pydantic import BaseSettings, Field


class PostgresConfig(BaseSettings):

    host: str = Field(
        default="127.0.0.1",
        env="postgres_host"
    )
    port: str = Field(
        default=5432,
        env="postgres_port"
    )
    name: str = Field(
        default="movie_database",
        env="postgres_name"
    )
    user: str = Field(
        default="postgres",
        env="postres_user"
    )
    password: str = Field(
        default=1234,
        env="postgres_password"
    )

    @property
    def dsn(self) -> str:
        dsn = "postgresql://{}:{}@{}:{}/{}".format(
            self.user,
            self.password,
            self.host,
            self.port,
            self.name
        )
        return dsn


class TelegramConfig(BaseSettings):

    token: str = Field(env="telegram_bot_token")


class Config:

    telegram: TelegramConfig = TelegramConfig()
    postgres: PostgresConfig = PostgresConfig()