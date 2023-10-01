from contextlib import asynccontextmanager
from dataclasses import dataclass
from typing import AsyncIterator

from asyncpg import Pool

from src.presentation.common.interfaces.dbr_gateway_factory import DatabaseReadingGatewayFactory
from src.infrastructure.application.dbr_gateway.asyncpg_impl import AsyncpgDatabaseReadingGateway


@dataclass(frozen=True, slots=True)
class AsyncpgDatabaseReadingGatewayFactory(DatabaseReadingGatewayFactory):

    pool: Pool

    @asynccontextmanager
    async def create_gateway(self) -> AsyncIterator[AsyncpgDatabaseReadingGateway]:
        async with self.pool.acquire() as connection:
            yield AsyncpgDatabaseReadingGateway(connection)