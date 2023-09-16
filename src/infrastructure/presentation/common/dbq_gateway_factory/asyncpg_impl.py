from dataclasses import dataclass
from typing import AsyncIterator
from contextlib import asynccontextmanager

from asyncpg import Pool

from src.main.common.gateway_factories import DatabaseQueriesGatewayFactory
from src.infrastructure.application.dbq_gateway.asyncpg_impl import AsyncpgDatabaseQueriesGateway


@dataclass(frozen=True, slots=True)
class AsyncpgDatabaseQueriesGatewayFactory(DatabaseQueriesGatewayFactory):

    pool: Pool

    @asynccontextmanager
    async def create_gateway(self) -> AsyncIterator[AsyncpgDatabaseQueriesGateway]:
        async with self.pool.acquire() as connection:
            yield AsyncpgDatabaseQueriesGateway(connection)