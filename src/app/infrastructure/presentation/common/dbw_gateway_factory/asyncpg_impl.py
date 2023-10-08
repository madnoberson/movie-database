from contextlib import asynccontextmanager
from dataclasses import dataclass
from typing import AsyncIterator

from asyncpg import Pool

from app.presentation.common.interfaces.dbw_gateway_factory import DatabaseWritingGatewayFactory
from app.infrastructure.application.dbw_gateway.asyncpg_impl import AsyncpgDatabaseWritingGateway


@dataclass(frozen=True, slots=True)
class AsyncpgDatabaseWritingGatewayFactory(DatabaseWritingGatewayFactory):

    pool: Pool

    @asynccontextmanager
    async def create_gateway(self) -> AsyncIterator[AsyncpgDatabaseWritingGateway]:
        async with self.pool.acquire() as connection:
            async with connection.transaction() as transaction:
                yield AsyncpgDatabaseWritingGateway(connection, transaction)