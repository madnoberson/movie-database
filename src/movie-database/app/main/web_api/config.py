import os
from dataclasses import dataclass
from typing import TypeVar, Callable


__all__ = (
    "load_config", "Config", "FastAPIConfig",
    "UvicornConfig", "PostgresConfig", "SessionGatewayConfig"
)


@dataclass(frozen=True, slots=True)
class Config:

    fastapi: "FastAPIConfig"
    uvicorn: "UvicornConfig"
    postgres: "PostgresConfig"
    session_gateway: "SessionGatewayConfig"


def load_config() -> Config:
    fastapi_config = load_fastapi_config(
        title_env="FASTAPI_TITLE", version_env="FASTAPI_VERSION",
        description_env="FASTAPI_DESCRIPTION", summary_env="FASTAPI_SUMMARY",
        docs_url_env="FASTAPI_DOCS_URL", redoc_url_env="FASTAPI_REDOC_URL"
    )
    uvicorn_config = load_uvicorn_config(
        host_env="UVICORN_HOST", port_env="UVICORN_PORT"
    )
    postgres_config = load_postgres_config(
        host_env="POSTGRES_HOST", port_env="POSTGRES_PORT", name_env="POSTGRES_NAME",
        user_env="POSTGRES_USER", password_env="POSTGRES_PASSWORD"
    )
    session_gateway_config = load_session_gateway_config(
        redis_host_env="SESSION_GATEWAY_REDIS_HOST",
        redis_port_env="SESSION_GATEWAY_REDIS_PORT",
        redis_db_env="SESSION_GATEWAY_REDIS_DB"
    )

    return Config(
        fastapi=fastapi_config, uvicorn=uvicorn_config,
        postgres=postgres_config, session_gateway=session_gateway_config
    )


V = TypeVar("V")
R = TypeVar("R")
D = TypeVar("D")


def get_env(
    key: str, result_factory: Callable[[V], R] = None,
    raise_if_not_exist: bool = False, default: D = None
) -> R | D:
    if (value := os.getenv(key)) is None and raise_if_not_exist:
        raise ValueError(f"Variable '{key}' is not set")
    return result_factory(value) if None not in (value, result_factory) else default


@dataclass(frozen=True, slots=True)
class FastAPIConfig:

    title: str
    version: str
    description: str
    summary: str
    docs_url: str
    redoc_url: str


def load_fastapi_config(
    title_env: str, version_env: str,
    description_env: str, summary_env: str,
    docs_url_env: str, redoc_url_env: str
) -> FastAPIConfig:
    return FastAPIConfig(
        title=get_env(title_env, default="Movie database"),
        version=get_env(version_env, default="0.1.0"),
        description=get_env(description_env, default=""),
        summary=get_env(summary_env, default=""),
        docs_url=get_env(docs_url_env, default="/docs"),
        redoc_url=get_env(redoc_url_env, default="/redoc")
    )


@dataclass(frozen=True, slots=True)
class UvicornConfig:

    host: str
    port: int


def load_uvicorn_config(host_env: str, port_env: str) -> UvicornConfig:
    return UvicornConfig(
        host=get_env(host_env, default="127.0.0.1"),
        port=get_env(port_env, int, default=8000)
    )


@dataclass(frozen=True, slots=True)
class PostgresConfig:

    host: str
    port: int
    name: str
    user: str
    password: str

    @property
    def dsn(self) -> str:
        return "postgresql://{}:{}@{}:{}/{}".format(
            self.user, self.password, self.host, self.port, self.name
        )


def load_postgres_config(
    host_env: str, port_env: str,
    name_env: str, user_env: str,
    password_env: str
) -> PostgresConfig:
    return PostgresConfig(
        host=get_env(host_env, default="127.0.0.1"),
        port=get_env(port_env, int, default=5432),
        name=get_env(name_env, default="movie_database"),
        user=get_env(user_env, default="postgres"),
        password=get_env(password_env, default="1234")
    )


@dataclass(frozen=True, slots=True)
class SessionGatewayConfig:

    redis_host: str
    redis_port: int
    redis_db: int


def load_session_gateway_config(
    redis_host_env: str, redis_port_env: str,
    redis_db_env: str
) -> SessionGatewayConfig:
    return SessionGatewayConfig(
        redis_host=get_env(redis_host_env, default="127.0.0.1"),
        redis_port=get_env(redis_port_env, int, default=6379),
        redis_db=get_env(redis_db_env, int, default=0)
    )
