from uvicorn import Server, Config
from fastapi import FastAPI


def create_server(app: FastAPI) -> Server:
    config = Config(app)
    server = Server(config)

    return server