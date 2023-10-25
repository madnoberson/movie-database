import json

from asyncpg.connection import Connection
from asyncpg.pool import Pool, create_pool


async def set_connection_codecs(connection: Connection) -> None:
    await connection.set_type_codec(
        typename="JSON", schema="pg_catalog", encoder=json.dumps, decoder=json.loads
    )
    await connection.set_type_codec(
        typename="JSONB", schema="pg_catalog", encoder=json.dumps, decoder=json.loads
    )


async def create_database_connection_pool(
    postgres_dsn: str, min_size: int, max_size: int, max_queries: int,
    max_inactive_connection_lifetime: int
) -> Pool:
    return await create_pool(
        dsn=postgres_dsn, min_size=min_size, max_size=max_size, max_queries=max_queries,
        max_inactive_connection_lifetime=max_inactive_connection_lifetime,
        init=set_connection_codecs
    )