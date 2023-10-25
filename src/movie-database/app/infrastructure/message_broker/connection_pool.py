from aio_pika.pool import Pool
from aio_pika.robust_connection import RobustConnection, connect_robust


def create_event_bus_connection_pool(
    rq_host: str, rq_port: int, rq_login: str, rq_password: str | None,
    max_size: int
) -> Pool[RobustConnection]:
    async def connection_factory() -> RobustConnection:
        return await connect_robust(
            host=rq_host, port=rq_port, login=rq_login, password=rq_password
        )
    return Pool(connection_factory, max_size=max_size)