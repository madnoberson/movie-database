from app.application.common.interfaces.uow import UnitOfWork


class EventBusUnitOfWork(UnitOfWork):

    async def commit(self) -> None:
        ...
    
    async def rollback(self) -> None:
        ...