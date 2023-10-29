import os
from typing import TypeVar, Callable
from dataclasses import dataclass
from datetime import timedelta


__all__ = (
    "load_web_api_config",
    "load_message_broker_config",
    "FastAPIConfig",
    "UvicornConfig",
    "FastStreamConfig",
    "DatabaseConfig",
    "IdentityProviderConfig"
)


@dataclass(frozen=True, slots=True)
class WebApiConfig:

    database: "DatabaseConfig"

    fastapi: "FastAPIConfig"
    uvicorn: "UvicornConfig"
    identity_provider: "IdentityProviderConfig"


def load_web_api_config() -> WebApiConfig:
    fastapi_config = _load_fastapi_config(
        title_env="FASTAPI_TITLE", version_env="FASTAPI_VERSION",
        description_env="FASTAPI_DESCRIPTION", summary_env="FASTAPI_SUMMARY",
        docs_url_env="FASTAPI_DOCS_URL", redoc_url_env="FASTAPI_REDOC_URL"
    )
    uvicorn_config = _load_uvicorn_config(
        host_env="UVICORN_HOST", port_env="UVICORN_PORT"
    )
    database_config = _load_database_config(
        postgres_host_env="DB_POSTGRES_HOST", postgres_port_env="DB_POSTGRES_PORT",
        postgres_name_env="DB_POSTGRES_NAME", postgres_user_env="DB_POSTGRES_USER",
        postgres_password_env="DB_POSTGRES_PASSWORD", max_queries_env="DB_MAX_QUERIES",
        min_connections_env="DB_MIN_CONNECTIONS", max_connections_env="DB_MAX_CONNECTIONS",
    )
    identity_provider_config = _load_identity_provider_config(
        session_gateway_redis_host_env="IDENTITY_PROVIDER_SESSION_GATEWAY_REDIS_HOST",
        session_gateway_redis_db_env="IDENTITY_PROVIDER_SESSION_GATEWAY_REDIS_PORT",
        session_gateway_redis_port_env="IDENTITY_PROVIDER_SESSION_GATEWAY_REDIS_DB",
        session_gateway_redis_password_env="IDENTITY_PROVIDER_SESSION_GATEWAY_REDIS_PASSWORD",
        session_gateway_session_lifetime_env="IDENTITY_PROVIDER_SESSION_GATEWAY_SESSION_LIFETIME",
        access_policy_gateway_redis_host_env="IDENTITY_PROVIDER_ACCESS_POLICY_GATEWAY_REDIS_HOST",
        access_policy_gateway_redis_port_env="IDENTITY_PROVIDER_ACCESS_POLICY_GATEWAY_REDIS_PORT",
        access_policy_gateway_redis_db_env="IDENTITY_PROVIDER_ACCESS_POLICY_GATEWAY_REDIS_DB",
        access_policy_gateway_redis_password_env="IDENTITY_PROVIDER_ACCESS_POLICY_GATEWAY_REDIS_PASSWORD"
    )

    return WebApiConfig(
        database=database_config, fastapi=fastapi_config, uvicorn=uvicorn_config,
        identity_provider=identity_provider_config
    )


@dataclass(frozen=True, slots=True)
class MessageBrokerConfig:

    database: "DatabaseConfig"

    faststream: "FastStreamConfig"


def load_message_broker_config() -> MessageBrokerConfig:
    database_config = _load_database_config(
        postgres_host_env="DB_POSTGRES_HOST", postgres_port_env="DB_POSTGRES_PORT",
        postgres_name_env="DB_POSTGRES_NAME", postgres_user_env="DB_POSTGRES_USER",
        postgres_password_env="DB_POSTGRES_PASSWORD", max_queries_env="DB_MAX_QUERIES",
        min_connections_env="DB_MIN_CONNECTIONS", max_connections_env="DB_MAX_CONNECTIONS",
    )
    faststream_config = _load_faststream_config(
        title_env="FASTSTREAM_TITLE", version_env="FASTSTREAM_VERSION",
        description_env="FASTSTREAM_DESCRIPTION", rq_host_env="FASTSTREAM_RQ_HOST",
        rq_port_env="FASTSTREAM_RQ_PORT", rq_login_env="FASTSTREAM_RQ_LOGIN",
        rq_password_env="FASTSTREAM_RQ_PASSWORD"
    )

    return MessageBrokerConfig(database=database_config, faststream=faststream_config)


@dataclass(frozen=True, slots=True)
class FastAPIConfig:

    title: str
    version: str
    description: str
    summary: str
    docs_url: str
    redoc_url: str


def _load_fastapi_config(
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


def _load_uvicorn_config(host_env: str, port_env: str) -> UvicornConfig:
    return UvicornConfig(
        host=get_env(host_env, default="127.0.0.1"),
        port=get_env(port_env, int, default=8000)
    )


@dataclass(frozen=True, slots=True)
class FastStreamConfig:

    title: str
    version: str
    description: str
    rq_host: str
    rq_port: int
    rq_login: str
    rq_password: str


def _load_faststream_config(
    title_env: str, version_env: str,
    description_env: str, rq_host_env: str,
    rq_port_env: str, rq_login_env: str,
    rq_password_env: str
) -> FastStreamConfig:
    return FastStreamConfig(
        title=get_env(title_env, default="Movie database admin"),
        version=get_env(version_env, default="0.1.0"),
        description=get_env(description_env, default=""),
        rq_host=get_env(rq_host_env, default="127.0.0.1"),
        rq_port=get_env(rq_port_env, int, default=5672),
        rq_login=get_env(rq_login_env, default="guest"),
        rq_password=get_env(rq_password_env, default="guest")
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


def _load_database_config(
    postgres_host_env: str, postgres_port_env: str,
    postgres_name_env: str, postgres_user_env: str,
    postgres_password_env: str, max_queries_env: str,
    min_connections_env: str, max_connections_env: str,
    max_inactive_connection_lifetime_env: str
) -> DatabaseConfig:
    return DatabaseConfig(
        postgres_host=get_env(postgres_host_env, default="127.0.0.1"),
        postgres_port=get_env(postgres_port_env, int, default=5432),
        postgres_name=get_env(postgres_name_env, default="movie_database_admin"),
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
class IdentityProviderConfig:

    session_gateway_redis_host: str
    session_gateway_redis_port: int
    session_gateway_redis_db: int
    session_gateway_redis_password: str | None
    session_gateway_session_lifetime: timedelta

    access_policy_gateway_redis_host: str
    access_policy_gateway_redis_port: int
    access_policy_gateway_redis_db: int
    access_policy_gateway_redis_password: str | None


def _load_identity_provider_config(
    session_gateway_redis_host_env: str, session_gateway_redis_port_env: str,
    session_gateway_redis_db_env: str, session_gateway_redis_password_env: str,
    session_gateway_session_lifetime_env: str, access_policy_gateway_redis_host_env: str,
    access_policy_gateway_redis_port_env: str, access_policy_gateway_redis_db_env: str,
    access_policy_gateway_redis_password_env: str
) -> IdentityProviderConfig:
    return IdentityProviderConfig(
        session_gateway_redis_host=get_env(session_gateway_redis_host_env, default="127.0.0.1"),
        session_gateway_redis_port=get_env(session_gateway_redis_port_env, int, default=6379),
        session_gateway_redis_db=get_env(session_gateway_redis_db_env, int, default=1),
        session_gateway_redis_password_env=get_env(session_gateway_redis_password_env),
        session_gateway_session_lifetime=get_env(
            session_gateway_session_lifetime_env,
            lambda m: timedelta(minutes=int(m)), default=timedelta(hours=24)
        ),
        access_policy_gateway_redis_host=get_env(
            access_policy_gateway_redis_host_env, default="127.0.0.1"
        ),
        access_policy_gateway_redis_port=get_env(
            access_policy_gateway_redis_port_env, int, default=6379
        ),
        access_policy_gateway_redis_db=get_env(
            access_policy_gateway_redis_db_env, int, default=1
        ),
        access_policy_gateway_redis_password=get_env(access_policy_gateway_redis_password_env)
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