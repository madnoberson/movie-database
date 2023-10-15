from contextlib import asynccontextmanager
from typing import AsyncIterator

from asyncpg.pool import Pool
from asyncpg.connection import Connection

from .uow import AsyncpgUnitOfWork
from . import repositories
from . import readers


class AsyncpgFactoriesManager:

    def __init__(
        self,
        writing_connection_pool: Pool,
        reading_connection_pool: Pool
    ) -> None:
        self.writing_connection_pool = writing_connection_pool
        self.reading_connection_pool = reading_connection_pool

    @asynccontextmanager
    async def build_repository_factory(self) -> AsyncIterator["AsyncpgRepositoryFactory"]:
        async with self.writing_connection_pool.acquire() as connection:
            yield AsyncpgRepositoryFactory(connection)
    
    @asynccontextmanager
    async def build_reader_factory(self) -> AsyncIterator["AsyncpgReaderFactory"]:
        async with self.reading_connection_pool.acquire() as connection:
            yield AsyncpgReaderFactory(connection)


class AsyncpgRepositoryFactory:

    def __init__(self, connection: Connection) -> None:
        self.connection = connection

    def build_user_repo(self) -> repositories.AsyncpgUserRepository:
        return repositories.AsyncpgUserRepository(self.connection)

    def build_movie_repo(self) -> repositories.AsyncpgMovieRepository:
        return repositories.AsyncpgMovieRepository(self.connection)
    
    async def build_uow(self) -> AsyncpgUnitOfWork:
        transaction = self.connection.transaction()
        await transaction.start()
        return AsyncpgUnitOfWork(transaction)
        

class AsyncpgReaderFactory:

    def __init__(self, connection: Connection) -> None:
        self.connection = connection
    
    def build_authentication_reader(self) -> readers.AsyncpgAuthenticationReader:
        return readers.AsyncpgAuthenticationReader(self.connection)
    
    def build_user_reader(self) -> readers.AsyncpgUserReader:
        return readers.AsyncpgUserReader(self.connection)