from redis.asyncio import Redis


def create_session_gateway_connection(
    redis_host: str, redis_port: int, redis_db: int, redis_password: str | None
) -> Redis:
    return Redis(
        host=redis_host, port=redis_port, db=redis_db, password=redis_password,
        decode_responses=True
    )


def create_access_policy_gateway_connection(
    redis_host: str, redis_port: int, redis_db: int, redis_password: str | None
) -> Redis:
    return Redis(
        host=redis_host, port=redis_port, db=redis_db, password=redis_password,
        decode_responses=True
    )