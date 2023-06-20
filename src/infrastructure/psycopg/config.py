from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class PsycopgConfig:
    
    host: str = "localhost"
    port: str = 5432
    name: str = "movie_database"
    user: str = "postgres"
    password: str = 1234

    @property
    def dsn(self) -> str:
        dsn = "postgresql://{}:{}@{}:{}/{}".format(
            self.user,
            self.password,
            self.host,
            self.port,
            self.name
        )
        return dsn