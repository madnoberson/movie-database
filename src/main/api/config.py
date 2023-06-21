from datetime import timedelta

from pydantic import BaseSettings


class UvicornConfig(BaseSettings):

    host: str = "127.0.0.1"
    port: int = 8000
    loop: str = "uvicorn"


class FastAPIConfig(BaseSettings):

    title: str = "Movie Database"
    description: str = ""
    version: str = "0.1.0"


class AuthConfig(BaseSettings):

    secret: str = "secret"
    access_token_expires: timedelta = timedelta(minutes=15)
    refresh_token_expires: timedelta = timedelta(days=14)
    algorithm: str = "HS256"


class Config:

    uvicorn: UvicornConfig = UvicornConfig()
    fastapi: FastAPIConfig = FastAPIConfig()
    auth: AuthConfig = AuthConfig()