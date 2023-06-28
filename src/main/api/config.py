from datetime import timedelta

from pydantic import BaseSettings


class UvicornConfig(BaseSettings):

    uvicorn_host: str = "127.0.0.1"
    uvicorn_port: int = 8000
    uvicorn_loop: str = "uvicorn"


class FastAPIConfig(BaseSettings):

    fastapi_title: str = "Movie Database"
    fastapi_description: str = ""
    fastapi_version: str = "0.1.0"


class AuthConfig(BaseSettings):

    auth_secret: str = "secret"
    auth_access_token_expires: timedelta = timedelta(minutes=15)
    auth_refresh_token_expires: timedelta = timedelta(days=14)
    auth_algorithm: str = "HS256"


class PostgresConfig(BaseSettings):

    postgres_host: str = "127.0.0.1"
    postgres_port: str = 5432
    postgres_name: str = "movie_database"
    postgres_user: str = "postgres"
    postgres_password: str = 1234

    @property
    def dsn(self) -> str:
        dsn = "postgresql://{}:{}@{}:{}/{}".format(
            self.postgres_user,
            self.postgres_password,
            self.postgres_host,
            self.postgres_port,
            self.postgres_name
        )
        return dsn


class Config:

    uvicorn: UvicornConfig = UvicornConfig()
    fastapi: FastAPIConfig = FastAPIConfig()
    auth: AuthConfig = AuthConfig()
    postgres: PostgresConfig = PostgresConfig()