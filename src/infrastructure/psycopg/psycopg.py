import psycopg2
from psycopg2.extras import register_uuid
from psycopg2._psycopg import connection

from .config import PsycopgConfig


PsycopgConnection = connection


def build_psycopg2_connection() -> PsycopgConnection:
    config = PsycopgConfig()
    register_uuid()
    return psycopg2.connect(config.dsn)