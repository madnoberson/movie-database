from aio_pika.pool import Pool
from aio_pika.robust_connection import RobustConnection, connect_robust


async def create_event_bus_connection(
    rq_host: str, rq_port: int, rq_login: str, rq_password: str | None
) -> Pool[RobustConnection]:
    return await connect_robust(
        host=rq_host, port=rq_port, login=rq_login, password=rq_password
    )