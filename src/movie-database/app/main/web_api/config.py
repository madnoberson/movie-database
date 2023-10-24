import os
from dataclasses import dataclass

from pydantic import TypeAdapter


def load_config() -> "Config":
    config_data = {}
    for name, field_type in Config.__annotations__.items():
        value = TypeAdapter(field_type).validate_python(dict(os.environ))
        config_data.update({name: value})
    return Config(**config_data)


@dataclass(frozen=True, slots=True)
class FastAPIConfig:

    title: str = "Movie database"
    version: str = "0.1.0"
    description: str = ""
    summary: str = ""
    docs_url: str = "/docs"
    redoc_url: str = "/redoc"


@dataclass(frozen=True, slots=True)
class UvicornConfig:

    host: str = "127.0.0.1"
    port: int = 8000


@dataclass(frozen=True, slots=True)
class PostgresConfig:

    host: str = "127.0.0.1"
    port: int = 5432
    name: str = "movie_database"
    user: str = "postgres"
    password: str = "1234"

    @property
    def dsn(self) -> str:
        return "postgresql://{}:{}@{}:{}/{}".format(
            self.user, self.password, self.host, self.port, self.name
        )


@dataclass(frozen=True, slots=True)
class RedisConfig:

    host: str = "127.0.0.1"
    port: int = 6379
    db: int = 0


@dataclass(frozen=True, slots=True)
class Config:

    fastapi: FastAPIConfig
    uvicorn: UvicornConfig
    postgres: PostgresConfig
    redis: RedisConfig
