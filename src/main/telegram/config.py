from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class TelegramConfig:

    token: str


@dataclass(frozen=True, slots=True)
class PostgresConfig:

    host: str
    port: int
    name: str
    user: str
    pswd: str

    @property
    def dsn(self) -> str:
        return "postgresql://{}:{}@{}:{}/{}".format(
            self.user, self.pswd, self.host, self.port, self.name
        )


@dataclass(frozen=True, slots=True)
class Config:

    telegram: TelegramConfig
    postgres: PostgresConfig

