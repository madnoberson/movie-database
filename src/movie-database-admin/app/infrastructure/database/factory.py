from contextlib import asynccontextmanager
from typing import AsyncIterator

from asyncpg.pool import Pool
from asyncpg.connection import Connection

from .uow import RepositoryUnitOfWork
from . import repositories


class DatabaseFactoryManager:

    def __init__(
        self,
        repo_connection_pool: Pool,
        reader_connection_pool: Pool
    ) -> None:
        self.repo_connection_pool = repo_connection_pool
        self.reader_connection_pool = reader_connection_pool

    @asynccontextmanager
    async def build_repo_factory(self) -> AsyncIterator["RepositoryFactory"]:
        async with self.repo_connection_pool.acquire() as connection:
            yield RepositoryFactory(connection)


class RepositoryFactory:

    def __init__(self, connection: Connection) -> None:
        self.connection = connection

    def build_superuser_repo(self) -> repositories.SuperuserRepositoryImpl:
        return repositories.SuperuserRepositoryImpl(self.connection)

    async def build_uow(self) -> RepositoryUnitOfWork:
        transaction = self.connection.transaction()
        await transaction.start()
        return RepositoryUnitOfWork(transaction)