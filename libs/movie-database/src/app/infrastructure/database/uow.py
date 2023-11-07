from asyncpg.transaction import Transaction

from app.application.common.interfaces.uow import UnitOfWork


class AsyncpgUnitOfWork(UnitOfWork):

    def __init__(self, transaction: Transaction) -> None:
        self.transaction = transaction

    async def commit(self) -> None:
        await self.transaction.commit()

    async def rollback(self) -> None:
        await self.transaction.rollback()
        