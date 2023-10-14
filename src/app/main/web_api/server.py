from fastapi import FastAPI
from uvicorn import Server, Config

from .config import UvicornConfig


def create_server(app: FastAPI, uvicorn_config: UvicornConfig) -> Server:
    return Server(Config(app=app, host=uvicorn_config.host, port=uvicorn_config.port))