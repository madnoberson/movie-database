from dataclasses import dataclass, field
import os


@dataclass(frozen=True, slots=True)
class PostgresConfig:

    postgres_host: str = field(
        default_factory=lambda: os.getenv("postgres_host", "127.0.0.1"),
        init=False
    )
    postgres_port: str = field(
        default_factory=lambda: os.getenv("postgres_port", 5432),
        init=False
    )
    postgres_name: str = field(
        default_factory=lambda: os.getenv("postgres_name", "movie_database"),
        init=False
    )
    postgres_user: str = field(
        default_factory=lambda: os.getenv("postgres_user", "postgres"),
        init=False
    )
    postgres_password: str = field(
        default_factory=lambda: os.getenv("postgres_password", 1234),
        init=False,
        repr=False
    )

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