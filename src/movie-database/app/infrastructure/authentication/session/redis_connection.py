from redis.asyncio import Redis

def create_redis_connection(host: str, port: int, db: int) -> Redis:
    return Redis(host=host, port=port, db=db, decode_responses=True)