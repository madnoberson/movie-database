from aio_pika.pool import Pool
from aio_pika.robust_connection import RobustConnection, connect_robust


async def create_connection_pool(url: str, max_size: int = 2) -> Pool[RobustConnection]:
    async def connection_factory() -> RobustConnection:
        return await connect_robust(url=url)
    return await Pool(connection_factory, max_size=max_size)