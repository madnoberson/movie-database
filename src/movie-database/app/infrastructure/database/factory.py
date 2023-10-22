from contextlib import asynccontextmanager
from typing import AsyncIterator

from asyncpg.pool import Pool
from asyncpg.connection import Connection

from .uow import AsyncpgUnitOfWork
from . import repositories
from . import readers


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
    
    @asynccontextmanager
    async def build_reader_factory(self) -> AsyncIterator["ReaderFactory"]:
        async with self.reader_connection_pool.acquire() as connection:
            yield ReaderFactory(connection)


class RepositoryFactory:

    def __init__(self, connection: Connection) -> None:
        self.connection = connection

    def build_user_repo(self) -> repositories.UserRepositoryImpl:
        return repositories.UserRepositoryImpl(self.connection)

    def build_movie_repo(self) -> repositories.MovieRepositoryImpl:
        return repositories.MovieRepositoryImpl(self.connection)
    
    def build_adding_task_repo(self) -> repositories.AddingTaskRepositoryImpl:
        return repositories.AddingTaskRepositoryImpl(self.connection)
    
    async def build_uow(self) -> AsyncpgUnitOfWork:
        transaction = self.connection.transaction()
        await transaction.start()
        return AsyncpgUnitOfWork(transaction)
        

class ReaderFactory:

    def __init__(self, connection: Connection) -> None:
        self.connection = connection
    
    def build_auth_reader(self) -> readers.AuthnReaderImpl:
        return readers.AuthnReaderImpl(self.connection)
    
    def build_user_reader(self) -> readers.UserReaderImpl:
        return readers.UserReaderImpl(self.connection)