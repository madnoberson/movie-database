from dataclasses import dataclass
from typing import AsyncIterator
from contextlib import asynccontextmanager

from asyncpg import Pool

from src.main.telegram_admin.ioc import DatabaseGatewayFactory
from src.infrastructure.application.db_gateway.asyncpg_impl import AsyncpgDatabaseGateway


@dataclass(frozen=True, slots=True)
class AsyncpgDatabaseGatewayFactory(DatabaseGatewayFactory):

    pool: Pool  

    @asynccontextmanager
    async def create_gateway(self) -> AsyncIterator[AsyncpgDatabaseGateway]:
        async with self.pool.acquire() as connection:
            transaction = connection.transaction()
            await transaction.start()
            yield AsyncpgDatabaseGateway(connection, transaction)