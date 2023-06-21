from uvicorn import Server, Config
from fastapi import FastAPI

from .config import UvicornConfig


def create_server(
    app: FastAPI,
    uvicorn_config: UvicornConfig
) -> Server:
    config = Config(
        app=app,
        host=uvicorn_config.host,
        port=uvicorn_config.port,
        loop=uvicorn_config.loop
    )
    server = Server(config)

    return server