from app.application.common.interfaces.uow import UnitOfWork

from aio_pika.abc import AbstractTransaction


class EventBusUnitOfWork(UnitOfWork):

    def __init__(self, transaction: AbstractTransaction) -> None:
        self.transaction = transaction

    async def commit(self) -> None:
        await self.transaction.commit()
    
    async def rollback(self) -> None:
        await self.transaction.rollback()