from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class TelegramConfig:

    bot_token: str


@dataclass(frozen=True, slots=True)
class PostgresConfig:

    host: str = "127.0.0.1"
    port: int = "5432"
    name: str = "movie_database"
    user: str = "postgres"
    pswd: str = "1234"

    @property
    def dsn(self) -> str:
        return "postgresql://{}:{}@{}:{}/{}".format(
            self.user, self.pswd, self.host, self.port, self.name
        )


@dataclass(frozen=True, slots=True)
class Config:

    telegram: TelegramConfig
    postgres: PostgresConfig

