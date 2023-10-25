import os
from dataclasses import dataclass
from typing import TypeVar, Callable
from datetime import timedelta


__all__ = (
    "load_config", "Config", "FastAPIConfig",
    "UvicornConfig", "DatabaseConfig", "SessionGatewayConfig"
)


def load_config() -> "Config":
    fastapi_config = load_fastapi_config(
        title_env="FASTAPI_TITLE", version_env="FASTAPI_VERSION",
        description_env="FASTAPI_DESCRIPTION", summary_env="FASTAPI_SUMMARY",
        docs_url_env="FASTAPI_DOCS_URL", redoc_url_env="FASTAPI_REDOC_URL"
    )
    uvicorn_config = load_uvicorn_config(
        host_env="UVICORN_HOST", port_env="UVICORN_PORT"
    )
    database_config = load_database_config(
        postgres_host_env="DB_POSTGRES_HOST", postgres_port_env="DB_POSTGRES_PORT",
        postgres_name_env="DB_POSTGRES_NAME", postgres_user_env="DB_POSTGRES_USER",
        postgres_password_env="DB_POSTGRES_PASSWORD", max_queries_env="DB_MAX_QUERIES",
        min_connections_env="DB_MIN_CONNECTIONS", max_connections_env="DB_MAX_CONNECTIONS",
        max_inactive_connection_lifetime_env="DB_INACTIVE_CONNECTION_LIFETIME"
    )
    event_bus_config = load_event_bus_config(
        rq_host_env="EVENT_BUS_RQ_HOST", rq_port_env="EVENT_BUS_RQ_PORT",
        rq_login_env="EVENT_BUS_RQ_LOGIN", rq_password_env="EVENT_BUS_RQ_PASSWORD",
        max_connections_env="EVENT_BUS_MAX_CONNECTIONS"

    )
    session_gateway_config = load_session_gateway_config(
        redis_host_env="SESSION_GATEWAY_REDIS_HOST", redis_port_env="SESSION_GATEWAY_REDIS_PORT",
        redis_db_env="SESSION_GATEWAY_REDIS_DB", redis_password_env="SESSION_GATEWAY_REDIS_PASSWORD",
        session_lifetime_env="SESSION_GATEWAY_LIFETIME"
    )

    return Config(
        fastapi=fastapi_config, uvicorn=uvicorn_config, database=database_config,
        event_bus=event_bus_config, session_gateway=session_gateway_config
    )


@dataclass(frozen=True, slots=True)
class Config:

    fastapi: "FastAPIConfig"
    uvicorn: "UvicornConfig"
    database: "DatabaseConfig"
    event_bus: "EventBusConfig"
    session_gateway: "SessionGatewayConfig"


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
class DatabaseConfig:

    postgres_host: str
    postgres_port: int
    postgres_name: str
    postgres_user: str
    postgres_password: str
    max_queries: int
    min_connections: int
    max_connections: int
    max_inactive_connection_lifetime: int

    @property
    def postgres_dsn(self) -> str:
        return "postgresql://{}:{}@{}:{}/{}".format(
            self.postgres_user, self.postgres_password, self.postgres_host,
            self.postgres_port, self.postgres_name
        )


def load_database_config(
    postgres_host_env: str, postgres_port_env: str,
    postgres_name_env: str, postgres_user_env: str,
    postgres_password_env: str, max_queries_env: str,
    min_connections_env: str, max_connections_env: str,
    max_inactive_connection_lifetime_env: str
) -> DatabaseConfig:
    return DatabaseConfig(
        postgres_host=get_env(postgres_host_env, default="127.0.0.1"),
        postgres_port=get_env(postgres_port_env, int, default=5432),
        postgres_name=get_env(postgres_name_env, default="movie_database"),
        postgres_user=get_env(postgres_user_env, default="postgres"),
        postgres_password=get_env(postgres_password_env, default="1234"),
        max_queries=get_env(max_queries_env, int, default=50000),
        min_connections=get_env(min_connections_env, int, default=10),
        max_connections=get_env(max_connections_env, int, default=10),
        max_inactive_connection_lifetime=get_env(
            max_inactive_connection_lifetime_env, int, default=300
        )
    )


@dataclass(frozen=True, slots=True)
class EventBusConfig:

    rq_host: str
    rq_port: int
    rq_login: str
    rq_password: str
    max_connections: int


def load_event_bus_config(
    rq_host_env: str, rq_port_env: str,
    rq_login_env: str, rq_password_env: str,
    max_connections_env: str
) -> EventBusConfig:
    return EventBusConfig(
        rq_host=get_env(rq_host_env, default="127.0.0.1"),
        rq_port=get_env(rq_port_env, int, default=5672),
        rq_login=get_env(rq_login_env, default="guest"),
        rq_password=get_env(rq_password_env, default="guest"),
        max_connections=get_env(max_connections_env, int, default=2)
    )


@dataclass(frozen=True, slots=True)
class SessionGatewayConfig:

    redis_host: str
    redis_port: int
    redis_db: int
    redis_password: str | None
    session_lifetime: timedelta


def load_session_gateway_config(
    redis_host_env: str, redis_port_env: str,
    redis_db_env: str, redis_password_env: str,
    session_lifetime_env: str
) -> SessionGatewayConfig:
    return SessionGatewayConfig(
        redis_host=get_env(redis_host_env, default="127.0.0.1"),
        redis_port=get_env(redis_port_env, int, default=6379),
        redis_db=get_env(redis_db_env, int, default=0),
        redis_password=get_env(redis_password_env),
        session_lifetime=get_env(
            session_lifetime_env, lambda m: timedelta(minutes=m),
            default=timedelta(hours=24)
        )
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