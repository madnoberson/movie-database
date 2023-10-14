import asyncio

from app.application.common.protocols.uow import UnitOfWork


class UnitOfWorkImpl(UnitOfWork):

    def __init__(self, *uows: UnitOfWork) -> None:
        self._uows = uows
    
    async def commit(self) -> None:
        await asyncio.gather(*[uow.commit() for uow in self._uows])
    
    async def rollback(self) -> None:
        await asyncio.gather(*[uow.rollback() for uow in self._uows])
