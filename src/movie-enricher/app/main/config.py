import os
from dataclasses import dataclass
from typing import TypeVar, Callable


__all__ = (
    "load_config", "Config", "FastStreamConfig"
)


def load_config() -> "Config":
    faststream_config = load_faststream_config(
        title_env="FASTSTREAM_TITLE", version_env="FASTSTREAM_VERSION",
        description_env="FASTSTREAM_DESCRIPTION", rq_host_env="FASTSTREAM_RQ_HOST",
        rq_port_env="FASTSTREAM_RQ_PORT", rq_login_env="FASTSTREAM_RQ_LOGIN",
        rq_password_env="FASTSTREAM_RQ_PASSWORD"
    )
    return Config(faststream=faststream_config)


@dataclass(frozen=True, slots=True)
class Config:

    faststream: "FastStreamConfig"


@dataclass(frozen=True, slots=True)
class FastStreamConfig:

    title: str
    version: str
    description: str
    rq_host: str
    rq_port: int
    rq_login: str
    rq_password: str


def load_faststream_config(
    title_env: str, version_env: str,
    description_env: str, rq_host_env: str,
    rq_port_env: str, rq_login_env: str,
    rq_password_env: str
) -> FastStreamConfig:
    return FastStreamConfig(
        title=get_env(title_env, default="Movie enricher"),
        version=get_env(version_env, default="0.1.0"),
        description=get_env(description_env, default=""),
        rq_host=get_env(rq_host_env, default="127.0.0.1"),
        rq_port=get_env(rq_port_env, int, default=5672),
        rq_login=get_env(rq_login_env, default="guest"),
        rq_password=get_env(rq_password_env, default="guest")
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