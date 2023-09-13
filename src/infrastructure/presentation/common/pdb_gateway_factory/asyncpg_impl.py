from dataclasses import dataclass
from typing import AsyncIterator
from contextlib import asynccontextmanager

from asyncpg import Pool

from src.main.common.gateway_factories import PresentationDatabaseGatewayFactory
from src.infrastructure.application.pdb_gateway.asyncpg_impl import AsyncpgPresentationDatabaseGateway


@dataclass(frozen=True, slots=True)
class AsyncpgPresentationDatabaseGatewayFactory(PresentationDatabaseGatewayFactory):

    pool: Pool

    @asynccontextmanager
    async def create_gateway(self) -> AsyncIterator[AsyncpgPresentationDatabaseGateway]:
        async with self.pool.acquire() as connection:
            yield AsyncpgPresentationDatabaseGateway(connection)