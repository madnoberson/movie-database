import json
from datetime import datetime

from asyncpg.connection import Connection
from asyncpg.pool import Pool, create_pool


async def create_database_connection_pool(
    postgres_dsn: str, min_size: int, max_size: int, max_queries: int,
    max_inactive_connection_lifetime: int
) -> Pool:
    return await create_pool(
        dsn=postgres_dsn, min_size=min_size, max_size=max_size, max_queries=max_queries,
        max_inactive_connection_lifetime=max_inactive_connection_lifetime,
        init=_set_connection_codecs
    )


async def _set_connection_codecs(connection: Connection) -> None:
    await connection.set_type_codec(
        typename="JSON", schema="pg_catalog", encoder=json.dumps, decoder=json.loads
    )
    await connection.set_type_codec(
        typename="JSONB", schema="pg_catalog", encoder=json.dumps, decoder=json.loads
    )
    await connection.set_type_codec(
        typename="TIMESTAMPTZ", schema="pg_catalog", encoder=_timestamptz_encoder,
        decoder=_timestamptz_decoder
    )


def _timestamptz_encoder(dt_or_str: datetime | str):
    if isinstance(dt_or_str, str):
        return dt_or_str

    dt_str = str(dt_or_str.astimezone())
    return dt_str


def _timestamptz_decoder(dt_str: str):
    if "+" in dt_str:
        dt_str_splitted = dt_str.split("+")
        dt_str, _ = dt_str_splitted
    else:
        dt_str_splitted = dt_str.split("-")
        *dt_str_list, _ = dt_str_splitted
        dt_str = "-".join(dt_str_list)

    dt = datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S.%f")
    return dt
