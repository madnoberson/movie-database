import psycopg2
from psycopg2.extras import register_uuid
from psycopg2._psycopg import connection


PsycopgConnection = connection


def get_psycopg2_connection(dsn: str) -> PsycopgConnection:
    register_uuid()
    return psycopg2.connect(dsn)