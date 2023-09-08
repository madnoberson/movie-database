import os
from typing import Any


__all__ = ["TelegramConfig", "PostgresConfig", "Config"]


def getenv(key: str, default: Any = None) -> str | None:
    return os.getenv(key, default) or os.getenv(key.upper(), default)


class TelegramConfig:

    token: str = getenv("bot_token")


class PostgresConfig:

    host: str = getenv("postgres_host", "127.0.0.1")
    port: int = getenv("postgres_port", 5432)
    name: str = getenv("postgres_name", "movie_database")
    user: str = getenv("postgres_user", "postgres")
    pswd: str = getenv("postgres_pswd", "1234")

    @property
    def dsn(self) -> str:
        return "postgresql://{}:{}@{}:{}/{}".format(
            self.user, self.pswd, self.host, self.port, self.name
        )


class Config:

    telegram = TelegramConfig()
    postgres = PostgresConfig()